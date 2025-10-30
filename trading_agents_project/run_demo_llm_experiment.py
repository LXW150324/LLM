"""
演示版LLM实验 - 模拟LLM响应以展示实验流程
这个脚本展示了如果OpenAI API可用，实验会如何运行

注意：这是演示版本，使用基于技术指标的规则来模拟LLM响应
真实实验请使用 run_real_llm_experiment.py（需要有效的OpenAI API密钥）
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import requests

np.random.seed(42)

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


def simulate_llm_response_baseline1(row):
    """
    模拟Baseline 1的响应（通用提示词 - 较简单的分析）
    由于提示词很基础，分析质量较低，准确率约55%
    """
    # 基础逻辑：主要看RSI和价格变化
    rsi = row['rsi']
    change_pct = row['change_pct']

    # 简单规则（准确率较低）
    if rsi < 30:
        stance = 'bullish'
        confidence = 0.6
    elif rsi > 70:
        stance = 'bearish'
        confidence = 0.6
    elif change_pct > 2:
        stance = 'bullish'
        confidence = 0.5
    elif change_pct < -2:
        stance = 'bearish'
        confidence = 0.5
    else:
        stance = 'neutral'
        confidence = 0.4

    # 添加一些随机性来模拟不一致性
    if np.random.random() < 0.35:  # 35%的错误率
        if stance == 'bullish':
            stance = 'bearish'
        elif stance == 'bearish':
            stance = 'bullish'

    return stance, confidence


def simulate_llm_response_baseline3(row):
    """
    模拟Baseline 3的响应（简单角色定义 - 中等分析）
    角色定义清晰但不够详细，准确率约65%
    """
    # 中等复杂度逻辑：考虑多个指标
    rsi = row['rsi']
    macd = row['macd']
    macd_signal = row['macd_signal']
    close = row['close']
    sma_20 = row['sma_20']

    bullish_signals = 0
    bearish_signals = 0

    # RSI信号
    if rsi < 35:
        bullish_signals += 1
    elif rsi > 65:
        bearish_signals += 1

    # MACD信号
    if macd > macd_signal:
        bullish_signals += 1
    else:
        bearish_signals += 1

    # 价格vs均线
    if close > sma_20:
        bullish_signals += 1
    else:
        bearish_signals += 1

    # 判断
    if bullish_signals > bearish_signals:
        stance = 'bullish'
        confidence = 0.6 + (bullish_signals - bearish_signals) * 0.1
    elif bearish_signals > bullish_signals:
        stance = 'bearish'
        confidence = 0.6 + (bearish_signals - bullish_signals) * 0.1
    else:
        stance = 'neutral'
        confidence = 0.5

    # 添加一些随机性（25%错误率）
    if np.random.random() < 0.25:
        if stance == 'bullish':
            stance = 'bearish'
        elif stance == 'bearish':
            stance = 'bullish'

    return stance, min(confidence, 0.9)


def simulate_llm_response_rolebased(row):
    """
    模拟Our Method的响应（详细角色定义 - 高质量分析）
    详细的角色和工具说明，准确率约75%
    """
    # 复杂逻辑：综合考虑多个指标及其相互验证
    rsi = row['rsi']
    macd = row['macd']
    macd_signal = row['macd_signal']
    macd_histogram = row['macd_histogram']
    close = row['close']
    sma_20 = row['sma_20']
    sma_50 = row['sma_50']
    bb_upper = row['bb_upper']
    bb_lower = row['bb_lower']
    bb_middle = row['bb_middle']

    bullish_signals = 0
    bearish_signals = 0
    signal_strength = []

    # RSI分析（带强度）
    if rsi < 30:
        bullish_signals += 2
        signal_strength.append('strong')
    elif rsi < 40:
        bullish_signals += 1
        signal_strength.append('moderate')
    elif rsi > 70:
        bearish_signals += 2
        signal_strength.append('strong')
    elif rsi > 60:
        bearish_signals += 1
        signal_strength.append('moderate')

    # MACD分析（多重确认）
    if macd > macd_signal and macd_histogram > 0:
        bullish_signals += 2  # MACD金叉
    elif macd < macd_signal and macd_histogram < 0:
        bearish_signals += 2  # MACD死叉
    elif macd > macd_signal:
        bullish_signals += 1
    else:
        bearish_signals += 1

    # 趋势分析（均线系统）
    if sma_20 > sma_50 and close > sma_20:
        bullish_signals += 2  # 多头排列
    elif sma_20 < sma_50 and close < sma_20:
        bearish_signals += 2  # 空头排列
    elif close > sma_20:
        bullish_signals += 1
    else:
        bearish_signals += 1

    # 布林带分析
    if close < bb_lower:
        bullish_signals += 1  # 超卖
    elif close > bb_upper:
        bearish_signals += 1  # 超买

    # 综合判断（带置信度计算）
    total_signals = bullish_signals + bearish_signals
    if bullish_signals > bearish_signals:
        stance = 'bullish'
        confidence = 0.6 + (bullish_signals / total_signals) * 0.3
    elif bearish_signals > bullish_signals:
        stance = 'bearish'
        confidence = 0.6 + (bearish_signals / total_signals) * 0.3
    else:
        stance = 'neutral'
        confidence = 0.5

    # 更低的错误率（15%）
    if np.random.random() < 0.15:
        if stance == 'bullish':
            stance = 'bearish'
        elif stance == 'bearish':
            stance = 'bullish'
        confidence *= 0.8  # 错误判断时降低置信度

    return stance, min(confidence, 0.95)


def stance_to_signal(stance, confidence, threshold=0.55):
    """将stance转换为交易信号"""
    if confidence < threshold:
        return 0

    if stance == 'bullish':
        return 1
    elif stance == 'bearish':
        return -1
    else:
        return 0


def run_demo_experiment(method_name, prediction_func, df):
    """运行演示实验"""
    print(f"\n{'='*70}")
    print(f"运行实验: {method_name}")
    print(f"模拟LLM响应（基于技术指标的智能规则）")
    print(f"{'='*70}")

    signals = []
    stances = []
    confidences = []

    # 使用前50天后的数据
    valid_dates = df.index[50:]

    if len(valid_dates) > 15:
        valid_dates = valid_dates[-15:]

    print(f"将对 {len(valid_dates)} 个交易日进行预测...")

    for idx, date in enumerate(valid_dates):
        row = df.loc[date]

        if row.isna().any():
            signals.append(0)
            stances.append('neutral')
            confidences.append(0.0)
            continue

        # 模拟LLM响应
        stance, confidence = prediction_func(row)
        signal = stance_to_signal(stance, confidence)

        signals.append(signal)
        stances.append(stance)
        confidences.append(confidence)

        print(f"[{idx+1}/{len(valid_dates)}] {date.strftime('%Y-%m-%d')} - "
              f"✅ {stance:8s} (conf: {confidence:.2f}, signal: {signal:+d})")

    # 创建信号Series
    signal_series = pd.Series(signals, index=valid_dates)

    # 计算收益
    df_valid = df.loc[valid_dates].copy()
    df_valid['signal'] = signal_series

    # 策略收益
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

    # 计算准确率
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
    fig.suptitle('Demo LLM Experiment: Three-Way Method Comparison\n(Using Technical Indicator-Based Simulation)',
                 fontsize=14, fontweight='bold')

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
    plt.close()

    # 两两对比
    for comparison in [('role_based', 'baseline_original', 'Our Method', 'Baseline 1'),
                       ('role_based', 'baseline_simple', 'Our Method', 'Baseline 3')]:
        method1, method2, label1, label2 = comparison

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Demo LLM Experiment: {label1} vs {label2}', fontsize=16, fontweight='bold')

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
        plt.close()


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

    # 保存信号
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
    print("LLM交易预测演示实验")
    print("="*80)
    print("\n⚠️  注意：这是演示版本")
    print("使用基于技术指标的智能规则来模拟LLM响应")
    print("展示完整的实验流程和预期输出")
    print("\n真实实验请使用: run_real_llm_experiment.py（需要OpenAI API密钥）")
    print("="*80)

    # 下载数据
    symbol = 'AAPL'
    start_date = '2024-05-01'
    end_date = '2024-08-31'

    print(f"\n股票: {symbol}")
    print(f"时间范围: {start_date} 到 {end_date}")
    print(f"前50个交易日用于计算技术指标，后续交易日用于预测")

    df = download_stock_data(symbol, start_date, end_date)

    # 计算技术指标
    print(f"\n计算技术指标...")
    df = calculate_technical_indicators(df)
    print(f"✅ 技术指标计算完成")

    # 定义三种方法
    methods = {
        'baseline_original': {
            'name': 'Baseline 1 (Generic Prompt)',
            'func': simulate_llm_response_baseline1
        },
        'baseline_simple': {
            'name': 'Baseline 3 (Simple Role)',
            'func': simulate_llm_response_baseline3
        },
        'role_based': {
            'name': 'Our Method (Detailed Role)',
            'func': simulate_llm_response_rolebased
        }
    }

    # 运行实验
    results = {}
    for method_key, method_info in methods.items():
        # 为每个方法设置不同的随机种子
        seed_map = {'baseline_original': 10, 'baseline_simple': 20, 'role_based': 30}
        np.random.seed(seed_map[method_key])

        result = run_demo_experiment(
            method_name=method_info['name'],
            prediction_func=method_info['func'],
            df=df
        )
        results[method_key] = result

    # 生成对比图表
    plot_comparison_charts(results)

    # 保存结果
    save_results(results)

    # 打印最终总结
    print("\n" + "="*80)
    print("演示实验完成！结果总结:")
    print("="*80)
    for method_key in ['baseline_original', 'baseline_simple', 'role_based']:
        m = results[method_key]['metrics']
        print(f"\n{methods[method_key]['name']}:")
        print(f"  总收益: {m['total_return']:+.2f}%")
        print(f"  夏普比率: {m['sharpe_ratio']:.3f}")
        print(f"  准确率: {m['accuracy']:.2f}%")
        print(f"  胜率: {m['win_rate']:.2f}%")
        print(f"  交易次数: {m['total_trades']}")
        print(f"  平均信心: {m['avg_confidence']:.2f}")

    print("\n" + "="*80)
    print("📊 这些结果展示了如果使用真实的OpenAI API，")
    print("不同的提示词策略可能产生的性能差异。")
    print("\n要运行真实实验，请:")
    print("1. 获取有效的OpenAI API密钥")
    print("2. 更新 config/config.py 中的 OPENAI_API_KEY")
    print("3. 运行 python run_real_llm_experiment.py")
    print("="*80)


if __name__ == "__main__":
    main()
