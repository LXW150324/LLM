"""
真实LLM实验脚本 - 使用实际的OpenAI API调用
这个脚本会真正调用GPT模型来生成交易预测
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests
from openai import OpenAI
import time
import json
from config.config import config

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def download_stock_data(symbol, start_date, end_date):
    """下载股票数据"""
    print(f"📈 正在下载 {symbol} 的数据...")
    start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
    params = {'period1': start_ts, 'period2': end_ts, 'interval': '1d', 'events': 'history'}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        df.columns = [c.lower() for c in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        print(f"✅ 成功下载 {len(df)} 条数据")
        return df
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print(f"📊 使用模拟数据")
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        dates = dates[dates.dayofweek < 5]  # 只保留工作日
        np.random.seed(123)
        base_price = 150
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = base_price * (1 + returns).cumprod()
        volumes = np.random.randint(50000000, 150000000, len(dates))

        df = pd.DataFrame({
            'open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
            'high': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
            'low': prices * (1 + np.random.uniform(-0.02, 0, len(dates))),
            'close': prices,
            'volume': volumes
        }, index=dates)

        return df


def calculate_technical_indicators(df):
    """计算技术指标"""
    df = df.copy()

    # 价格变化
    df['returns'] = df['close'].pct_change()
    df['change_pct'] = (df['close'] - df['open']) / df['open'] * 100

    # 移动平均线
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()

    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']

    # 布林带
    df['bb_middle'] = df['close'].rolling(window=20).mean()
    bb_std = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
    df['bb_lower'] = df['bb_middle'] - (bb_std * 2)

    # 成交量变化
    df['volume_change_pct'] = df['volume'].pct_change() * 100

    return df


def get_baseline1_prompt():
    """Baseline 1: 最基础的通用提示词"""
    return """You are a stock market analyst. Analyze the given stock data and provide a trading recommendation.

Output your analysis as JSON with these fields:
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}"""


def get_baseline3_prompt():
    """Baseline 3: 简单的角色定义"""
    return """You are a Technical Analyst specializing in stock market analysis.

Your role:
- Analyze price trends and technical indicators
- Provide buy/sell/hold recommendations
- Assess market conditions

Output your analysis as JSON with these fields:
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "your analysis"
}"""


def get_rolebased_prompt():
    """Our Method: 详细的角色特定提示词（类似agents中的实现）"""
    return """You are an experienced Technical Analyst specializing in price trends and technical indicators.

Your responsibilities:
1. Analyze price trends (uptrend/downtrend/sideways)
2. Interpret technical indicators (RSI, MACD, Bollinger Bands, etc.)
3. Identify key support and resistance levels
4. Evaluate the strength of buy/sell signals

Technical analysis tools you use:
- Trend indicators: Moving averages, MACD
- Momentum indicators: RSI
- Volatility indicators: Bollinger Bands
- Volume indicators

Output your analysis as JSON with these fields:
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "trend_direction": "uptrend/downtrend/sideways",
    "trend_strength": "strong/moderate/weak",
    "key_signals": ["list of key technical signals"],
    "reasoning": "detailed technical analysis reasoning"
}

Important notes:
- Signals are more reliable when multiple indicators confirm each other
- Pay attention to divergence (price vs indicator inconsistency)
- Consider volume confirmation
- Base your analysis only on the provided technical data"""


def format_market_data(row, symbol='AAPL'):
    """格式化市场数据为LLM输入"""
    return f"""Analyze the following technical data for {symbol}:

Price Information:
- Current Price: ${row['close']:.2f}
- Open: ${row['open']:.2f}
- High: ${row['high']:.2f}
- Low: ${row['low']:.2f}
- Change: {row['change_pct']:+.2f}%
- Volume: {int(row['volume']):,}

Trend Indicators:
- 20-day SMA: ${row['sma_20']:.2f}
- 50-day SMA: ${row['sma_50']:.2f}
- EMA12: ${row['ema_12']:.2f}
- EMA26: ${row['ema_26']:.2f}

Momentum Indicators:
- RSI(14): {row['rsi']:.2f}
- MACD: {row['macd']:.4f}
- MACD Signal: {row['macd_signal']:.4f}
- MACD Histogram: {row['macd_histogram']:.4f}

Volatility Indicators:
- Bollinger Upper: ${row['bb_upper']:.2f}
- Bollinger Middle: ${row['bb_middle']:.2f}
- Bollinger Lower: ${row['bb_lower']:.2f}

Volume:
- Volume Change: {row['volume_change_pct']:+.2f}%

Please provide your trading recommendation based on this technical data."""


def call_gpt_for_prediction(system_prompt, user_message, client, max_retries=3):
    """调用GPT API获取预测"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # 使用GPT-4以获得更好的预测
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content
            return content

        except Exception as e:
            error_str = str(e)

            if "rate_limit" in error_str.lower() or "429" in error_str:
                wait_time = (attempt + 1) * 10
                print(f"⏳ API速率限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                print(f"❌ API调用错误: {error_str}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    raise

    raise Exception(f"调用GPT失败，已重试 {max_retries} 次")


def parse_llm_response(response_text):
    """解析LLM响应，提取stance和confidence"""
    try:
        # 尝试提取JSON
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)

            stance = result.get('stance', 'neutral').lower()
            confidence = float(result.get('confidence', 0.5))

            return stance, confidence
    except:
        pass

    # 如果JSON解析失败，使用关键词匹配
    text_lower = response_text.lower()

    if any(word in text_lower for word in ['bullish', 'buy', 'positive']):
        stance = 'bullish'
    elif any(word in text_lower for word in ['bearish', 'sell', 'negative']):
        stance = 'bearish'
    else:
        stance = 'neutral'

    # 默认confidence
    if 'very confident' in text_lower or 'highly confident' in text_lower:
        confidence = 0.9
    elif 'confident' in text_lower:
        confidence = 0.7
    else:
        confidence = 0.5

    return stance, confidence


def stance_to_signal(stance, confidence, threshold=0.6):
    """将stance转换为交易信号"""
    if confidence < threshold:
        return 0  # 信心不足，不交易

    if stance == 'bullish':
        return 1  # 买入
    elif stance == 'bearish':
        return -1  # 卖出
    else:
        return 0  # 中性，不交易


def run_llm_experiment(method_name, system_prompt, df, symbol, client):
    """运行真实的LLM实验"""
    print(f"\n{'='*70}")
    print(f"运行实验: {method_name}")
    print(f"使用真实的OpenAI API调用")
    print(f"{'='*70}")

    signals = []
    stances = []
    confidences = []

    # 只使用有足够历史数据的日期（跳过前50天用于计算指标）
    valid_dates = df.index[50:]

    # 为了控制成本，只预测最后15个交易日
    if len(valid_dates) > 15:
        valid_dates = valid_dates[-15:]

    print(f"将对 {len(valid_dates)} 个交易日进行预测...")

    for idx, date in enumerate(valid_dates):
        row = df.loc[date]

        # 跳过有NaN的行
        if row.isna().any():
            signals.append(0)
            stances.append('neutral')
            confidences.append(0.0)
            continue

        # 格式化输入数据
        user_message = format_market_data(row, symbol)

        # 调用GPT
        try:
            print(f"[{idx+1}/{len(valid_dates)}] {date.strftime('%Y-%m-%d')} - 调用GPT API...", end=' ')
            response = call_gpt_for_prediction(system_prompt, user_message, client)

            # 解析响应
            stance, confidence = parse_llm_response(response)
            signal = stance_to_signal(stance, confidence)

            signals.append(signal)
            stances.append(stance)
            confidences.append(confidence)

            print(f"✅ {stance} (conf: {confidence:.2f}, signal: {signal:+d})")

            # 为了避免速率限制，添加小延迟
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ 失败: {e}")
            signals.append(0)
            stances.append('neutral')
            confidences.append(0.0)

    # 创建信号Series
    signal_series = pd.Series(signals, index=valid_dates)

    # 计算收益
    df_valid = df.loc[valid_dates].copy()
    df_valid['signal'] = signal_series

    # 策略收益 = 信号 * 未来收益
    df_valid['strategy_returns'] = df_valid['signal'].shift(1) * df_valid['returns']
    df_valid = df_valid.dropna()

    # 计算指标
    strategy_returns = df_valid['strategy_returns']

    total_return = (1 + strategy_returns).prod() - 1
    sharpe = (strategy_returns.mean() * 252) / (strategy_returns.std() * np.sqrt(252)) if strategy_returns.std() > 0 else 0

    cumulative = (1 + strategy_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    win_trades = (strategy_returns > 0).sum()
    total_trades = (df_valid['signal'] != 0).sum()
    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0

    # 计算准确率（信号方向与实际收益方向一致）
    correct_predictions = (
        ((df_valid['signal'] > 0) & (df_valid['returns'] > 0)) |
        ((df_valid['signal'] < 0) & (df_valid['returns'] < 0)) |
        ((df_valid['signal'] == 0) & (df_valid['returns'].abs() < 0.003))
    )
    accuracy = (correct_predictions.sum() / len(df_valid) * 100)

    volatility = strategy_returns.std() * np.sqrt(252) * 100

    metrics = {
        'total_return': total_return * 100,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown * 100,
        'win_rate': win_rate,
        'accuracy': accuracy,
        'total_trades': int(total_trades),
        'volatility': volatility,
        'avg_confidence': np.mean(confidences)
    }

    print(f"\n实验结果:")
    print(f"  总收益率: {metrics['total_return']:.2f}%")
    print(f"  夏普比率: {metrics['sharpe_ratio']:.3f}")
    print(f"  最大回撤: {metrics['max_drawdown']:.2f}%")
    print(f"  准确率: {metrics['accuracy']:.2f}%")
    print(f"  胜率: {metrics['win_rate']:.2f}%")
    print(f"  总交易次数: {metrics['total_trades']}")
    print(f"  平均信心度: {metrics['avg_confidence']:.2f}")

    return {
        'method': method_name,
        'metrics': metrics,
        'signals': signal_series,
        'stances': stances,
        'confidences': confidences
    }


def plot_comparison_charts(results):
    """生成对比图表"""
    print(f"\n{'='*70}")
    print("生成对比图表...")
    print(f"{'='*70}")

    methods = ['baseline_original', 'baseline_simple', 'role_based']
    labels = ['Baseline 1\n(Generic)', 'Baseline 3\n(Simple Role)', 'Our Method\n(Detailed Role)']
    colors = ['#ff6b6b', '#feca57', '#48dbfb']

    # 三方对比图
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Real LLM Experiment: Three-Way Method Comparison', fontsize=16, fontweight='bold')

    metrics_list = [results[m]['metrics'] for m in methods]

    metrics_to_plot = [
        ('total_return', 'Total Return (%)', '(A) Total Return'),
        ('sharpe_ratio', 'Sharpe Ratio', '(B) Sharpe Ratio'),
        ('max_drawdown', 'Max Drawdown (%)', '(C) Max Drawdown'),
        ('accuracy', 'Accuracy (%)', '(D) Accuracy'),
        ('win_rate', 'Win Rate (%)', '(E) Win Rate'),
        ('avg_confidence', 'Avg Confidence', '(F) Average Confidence')
    ]

    for idx, (metric_key, ylabel, title) in enumerate(metrics_to_plot):
        row = idx // 3
        col = idx % 3
        ax = axes[row, col]

        values = [m[metric_key] for m in metrics_list]
        bars = ax.bar(range(3), values, color=colors, alpha=0.7, edgecolor='black')
        ax.set_xticks(range(3))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylabel(ylabel, fontweight='bold')
        ax.set_title(title, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h,
                   f'{h:.2f}', ha='center',
                   va='bottom' if h > 0 else 'top', fontsize=9)

    plt.tight_layout()
    plt.savefig('comparison_all_three_methods.png', dpi=300, bbox_inches='tight')
    print("✅ 已保存: comparison_all_three_methods.png")

    # 两两对比图
    for comparison in [('role_based', 'baseline_original', 'Our Method', 'Baseline 1'),
                       ('role_based', 'baseline_simple', 'Our Method', 'Baseline 3')]:
        method1, method2, label1, label2 = comparison

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Real LLM Experiment: {label1} vs {label2}', fontsize=16, fontweight='bold')

        m1 = results[method1]['metrics']
        m2 = results[method2]['metrics']

        # 收益对比
        ax = axes[0, 0]
        bars = ax.bar([0, 1], [m1['total_return'], m2['total_return']],
                      color=['#48dbfb', '#ff6b6b'], alpha=0.7, edgecolor='black')
        ax.set_xticks([0, 1])
        ax.set_xticklabels([label1, label2])
        ax.set_ylabel('Total Return (%)', fontweight='bold')
        ax.set_title('(A) Total Return', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.2f}%',
                    ha='center', va='bottom' if h > 0 else 'top')

        # 夏普比率和胜率
        ax = axes[0, 1]
        x = np.arange(2)
        width = 0.35
        bars1 = ax.bar(x - width/2, [m1['sharpe_ratio'], m2['sharpe_ratio']],
                      width, label='Sharpe Ratio', color='#1dd1a1', alpha=0.7)
        ax2 = ax.twinx()
        bars2 = ax2.bar(x + width/2, [m1['win_rate'], m2['win_rate']],
                       width, label='Win Rate (%)', color='#5f27cd', alpha=0.7)
        ax.set_ylabel('Sharpe Ratio', fontweight='bold')
        ax2.set_ylabel('Win Rate (%)', fontweight='bold')
        ax.set_title('(B) Risk-Adjusted Performance', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([label1, label2])
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)

        # 准确率对比
        ax = axes[1, 0]
        bars = ax.bar([0, 1], [m1['accuracy'], m2['accuracy']],
                      color=['#ee5a6f', '#0abde3'], alpha=0.7, edgecolor='black')
        ax.set_xticks([0, 1])
        ax.set_xticklabels([label1, label2])
        ax.set_ylabel('Accuracy (%)', fontweight='bold')
        ax.set_title('(C) Prediction Accuracy', fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h, f'{h:.1f}%',
                    ha='center', va='bottom')

        # 信号累积
        ax = axes[1, 1]
        sig1 = results[method1]['signals']
        sig2 = results[method2]['signals']
        cum1 = sig1.cumsum()
        cum2 = sig2.cumsum()
        ax.plot(cum1.index, cum1, label=label1, color='#48dbfb', linewidth=2)
        ax.plot(cum2.index, cum2, label=label2, color='#ff6b6b', linewidth=2)
        ax.set_ylabel('Cumulative Signals', fontweight='bold')
        ax.set_title('(D) Signal Accumulation', fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()
        filename = f"comparison_ours_vs_{method2.replace('baseline_', 'baseline')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✅ 已保存: {filename}")


def save_results(results):
    """保存实验结果"""
    print(f"\n{'='*70}")
    print("保存实验结果...")
    print(f"{'='*70}")

    # 保存汇总CSV
    summary_data = []
    for method, result in results.items():
        m = result['metrics']
        summary_data.append({
            'Method': method,
            'Total Return (%)': m['total_return'],
            'Sharpe Ratio': m['sharpe_ratio'],
            'Max Drawdown (%)': m['max_drawdown'],
            'Accuracy (%)': m['accuracy'],
            'Win Rate (%)': m['win_rate'],
            'Total Trades': m['total_trades'],
            'Volatility (%)': m['volatility'],
            'Avg Confidence': m['avg_confidence']
        })

    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv('experiment_summary.csv', index=False)
    print("✅ 已保存: experiment_summary.csv")

    # 保存每个方法的信号
    for method, result in results.items():
        filename = f'signals_{method}.csv'
        pd.DataFrame({
            'date': result['signals'].index,
            'signal': result['signals'].values
        }).to_csv(filename, index=False)
        print(f"✅ 已保存: {filename}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print("真实LLM交易预测实验")
    print("="*80)
    print("\n⚠️  注意：这个实验会使用真实的OpenAI API调用")
    print("每次预测都会调用GPT-4模型")
    print("预计API费用: $2-5 (取决于交易日数量)")
    print("="*80)

    # 确认API密钥
    api_key = config.OPENAI_API_KEY
    if not api_key or api_key.startswith('your-'):
        print("\n❌ 错误: 未找到有效的OpenAI API密钥")
        print("请在 config/config.py 中设置 OPENAI_API_KEY")
        return

    # 初始化OpenAI客户端
    client = OpenAI(api_key=api_key)
    print(f"\n✅ OpenAI客户端已初始化")

    # 下载数据
    symbol = 'AAPL'
    start_date = '2024-05-01'
    end_date = '2024-08-31'  # 使用4个月的数据（约80个交易日）

    print(f"\n股票: {symbol}")
    print(f"时间范围: {start_date} 到 {end_date}")
    print(f"前50个交易日用于计算技术指标，后续交易日用于LLM预测")

    df = download_stock_data(symbol, start_date, end_date)

    # 计算技术指标
    print(f"\n计算技术指标...")
    df = calculate_technical_indicators(df)
    print(f"✅ 技术指标计算完成")

    # 定义三种方法
    methods = {
        'baseline_original': {
            'name': 'Baseline 1 (Generic Prompt)',
            'prompt': get_baseline1_prompt()
        },
        'baseline_simple': {
            'name': 'Baseline 3 (Simple Role)',
            'prompt': get_baseline3_prompt()
        },
        'role_based': {
            'name': 'Our Method (Detailed Role)',
            'prompt': get_rolebased_prompt()
        }
    }

    # 运行实验
    results = {}
    for method_key, method_info in methods.items():
        try:
            result = run_llm_experiment(
                method_name=method_info['name'],
                system_prompt=method_info['prompt'],
                df=df,
                symbol=symbol,
                client=client
            )
            results[method_key] = result
        except Exception as e:
            print(f"\n❌ 实验 {method_key} 失败: {e}")
            import traceback
            traceback.print_exc()

    if len(results) < 3:
        print("\n❌ 部分实验失败，无法生成完整对比")
        return

    # 生成对比图表
    plot_comparison_charts(results)

    # 保存结果
    save_results(results)

    # 打印最终总结
    print("\n" + "="*80)
    print("实验完成！结果总结:")
    print("="*80)
    for method_key in ['baseline_original', 'baseline_simple', 'role_based']:
        m = results[method_key]['metrics']
        print(f"\n{methods[method_key]['name']}:")
        print(f"  总收益: {m['total_return']:+.2f}%")
        print(f"  夏普比率: {m['sharpe_ratio']:.3f}")
        print(f"  准确率: {m['accuracy']:.2f}%")
        print(f"  胜率: {m['win_rate']:.2f}%")
        print(f"  交易次数: {m['total_trades']}")

    print("\n" + "="*80)
    print("✅ 所有结果已保存")
    print("="*80)


if __name__ == "__main__":
    main()
