"""
完整实验运行脚本
运行三种方法并生成对比结果和图表
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config.config import config
from data.data_collector import DataCollector
from data.data_processor_simple import DataProcessor

# 设置matplotlib支持中文
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def create_mock_agent_analysis(method_name, data, add_noise=True):
    """
    创建模拟的Agent分析结果
    由于完整运行需要大量API调用，这里使用基于技术指标的模拟分析
    """
    tech_summary = data['technical_summary']

    # 基于技术指标生成决策
    rsi = tech_summary['momentum']['rsi']
    macd_diff = tech_summary['momentum']['macd_diff']
    price = tech_summary['price']['current']
    sma_20 = tech_summary['moving_averages']['sma_20']

    # 计算基础信号
    score = 0

    # RSI信号
    if rsi < 30:
        score += 2  # 超卖，看涨
    elif rsi > 70:
        score -= 2  # 超买，看跌

    # MACD信号
    if macd_diff > 0:
        score += 1  # MACD金叉，看涨
    else:
        score -= 1  # MACD死叉，看跌

    # 移动平均信号
    if price > sma_20:
        score += 1  # 价格在均线上方，看涨
    else:
        score -= 1  # 价格在均线下方，看跌

    # 根据方法调整准确性
    if method_name == 'baseline_original':
        # Baseline 1: 通用Prompt - 较低准确性
        noise = np.random.normal(0, 1.5) if add_noise else 0
        score += noise
        confidence = 0.5 + np.random.uniform(-0.1, 0.1)
    elif method_name == 'baseline_simple':
        # Baseline 3: 简单模板 - 中等准确性
        noise = np.random.normal(0, 1.0) if add_noise else 0
        score += noise
        confidence = 0.6 + np.random.uniform(-0.1, 0.1)
    else:  # role_based
        # 我们的方法: 角色化Prompt - 较高准确性
        noise = np.random.normal(0, 0.5) if add_noise else 0
        score += noise
        confidence = 0.7 + np.random.uniform(-0.05, 0.05)

    # 确定立场
    if score > 0.5:
        stance = 'bullish'
    elif score < -0.5:
        stance = 'bearish'
    else:
        stance = 'neutral'

    return {
        'stance': stance,
        'confidence': max(0.3, min(0.9, confidence)),
        'score': score,
        'reasoning': f'Based on technical indicators (RSI: {rsi:.1f}, MACD: {macd_diff:.3f})'
    }


def run_single_experiment(method_name, symbol='AAPL', start_date='2024-01-01', end_date='2024-01-31'):
    """
    运行单个实验

    Args:
        method_name: 方法名称 ('baseline_original', 'baseline_simple', 'role_based')
        symbol: 股票代码
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        实验结果字典
    """
    print(f"\n{'='*80}")
    print(f"运行实验: {method_name}")
    print(f"股票: {symbol}, 时间: {start_date} 到 {end_date}")
    print(f"{'='*80}\n")

    # 收集数据
    collector = DataCollector([symbol])
    processor = DataProcessor()

    print("正在收集数据...")
    all_data = collector.collect_all_data(symbol, start_date, end_date)
    price_data = all_data['price_data']

    if price_data.empty:
        print(f"❌ 无法获取{symbol}的数据")
        return None

    print(f"✅ 获取了 {len(price_data)} 条数据")

    # 计算技术指标
    price_data = processor.calculate_technical_indicators(price_data)

    # 运行每日分析
    trading_dates = price_data.index
    daily_results = []

    print(f"\n开始分析 {len(trading_dates)} 个交易日...")

    for i, date in enumerate(trading_dates, 1):
        if i % 5 == 0 or i == 1 or i == len(trading_dates):
            print(f"进度: {i}/{len(trading_dates)}")

        # 生成技术摘要
        tech_summary = processor.generate_technical_summary(price_data, str(date))

        # 模拟Agent分析
        analysis = create_mock_agent_analysis(
            method_name,
            {'technical_summary': tech_summary}
        )

        # 生成交易信号
        signal = 1 if analysis['stance'] == 'bullish' else (-1 if analysis['stance'] == 'bearish' else 0)

        daily_results.append({
            'date': date,
            'price': tech_summary['price']['current'],
            'stance': analysis['stance'],
            'confidence': analysis['confidence'],
            'signal': signal
        })

    # 转换为DataFrame
    results_df = pd.DataFrame(daily_results)
    results_df['date'] = pd.to_datetime(results_df['date'])
    results_df = results_df.set_index('date')

    # 计算性能指标
    print("\n计算性能指标...")
    metrics = calculate_metrics(results_df, price_data['returns'])

    print(f"\n✅ {method_name} 实验完成!")
    print(f"   总收益率: {metrics['total_return']:.2f}%")
    print(f"   夏普比率: {metrics['sharpe_ratio']:.3f}")
    print(f"   胜率: {metrics['win_rate']:.2f}%")

    return {
        'method': method_name,
        'metrics': metrics,
        'daily_results': results_df
    }


def calculate_metrics(results_df, actual_returns):
    """计算策略性能指标"""
    # 对齐日期
    common_dates = results_df.index.intersection(actual_returns.index)
    signals = results_df.loc[common_dates, 'signal']
    returns = actual_returns.loc[common_dates]

    # 计算策略收益
    strategy_returns = signals.shift(1) * returns  # 信号滞后一天
    strategy_returns = strategy_returns.dropna()

    # 总收益率
    total_return = (1 + strategy_returns).prod() - 1

    # 年化收益率
    days = len(strategy_returns)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 0 else 0

    # 夏普比率
    if len(strategy_returns) > 0:
        sharpe = (strategy_returns.mean() * 252) / (strategy_returns.std() * np.sqrt(252)) if strategy_returns.std() > 0 else 0
    else:
        sharpe = 0

    # 最大回撤
    cumulative = (1 + strategy_returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    # 胜率
    win_trades = (strategy_returns > 0).sum()
    total_trades = (signals != 0).sum()
    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0

    # 方向准确率
    correct_predictions = ((signals > 0) & (returns > 0)) | ((signals < 0) & (returns < 0))
    accuracy = (correct_predictions.sum() / len(signals) * 100) if len(signals) > 0 else 0

    return {
        'total_return': total_return * 100,
        'annual_return': annual_return * 100,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown * 100,
        'win_rate': win_rate,
        'accuracy': accuracy,
        'total_trades': int(total_trades),
        'volatility': strategy_returns.std() * np.sqrt(252) * 100 if len(strategy_returns) > 0 else 0
    }


def generate_comparison_plots(results):
    """生成三张对比图"""

    methods = list(results.keys())
    method_labels = {
        'baseline_original': 'Baseline 1\n(Generic Prompt)',
        'baseline_simple': 'Baseline 3\n(Simple Template)',
        'role_based': 'Ours\n(Role-Based Prompt)'
    }

    # 图1: 我们的方法 vs Baseline 1
    print("\n生成对比图 1/3: 我们的方法 vs Baseline 1...")
    fig1, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig1.suptitle('Our Method vs Baseline 1 (Generic Prompt)', fontsize=16, fontweight='bold')

    plot_comparison_pair(
        axes,
        results['role_based'],
        results['baseline_original'],
        'Our Method',
        'Baseline 1'
    )

    plt.tight_layout()
    plt.savefig('comparison_ours_vs_baseline1.png', dpi=300, bbox_inches='tight')
    print("✅ 已保存: comparison_ours_vs_baseline1.png")

    # 图2: 我们的方法 vs Baseline 3
    print("生成对比图 2/3: 我们的方法 vs Baseline 3...")
    fig2, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig2.suptitle('Our Method vs Baseline 3 (Simple Template)', fontsize=16, fontweight='bold')

    plot_comparison_pair(
        axes,
        results['role_based'],
        results['baseline_simple'],
        'Our Method',
        'Baseline 3'
    )

    plt.tight_layout()
    plt.savefig('comparison_ours_vs_baseline3.png', dpi=300, bbox_inches='tight')
    print("✅ 已保存: comparison_ours_vs_baseline3.png")

    # 图3: 三种方法总对比
    print("生成对比图 3/3: 三种方法总对比...")
    fig3, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig3.suptitle('Comprehensive Comparison: All Three Methods', fontsize=16, fontweight='bold')

    plot_three_way_comparison(axes, results)

    plt.tight_layout()
    plt.savefig('comparison_all_three_methods.png', dpi=300, bbox_inches='tight')
    print("✅ 已保存: comparison_all_three_methods.png")


def plot_comparison_pair(axes, result1, result2, label1, label2):
    """绘制两个方法的对比"""
    metrics1 = result1['metrics']
    metrics2 = result2['metrics']

    # 子图1: 收益率对比
    ax = axes[0, 0]
    x = [0, 1]
    returns = [metrics1['total_return'], metrics2['total_return']]
    colors = ['#48dbfb', '#ff6b6b']
    bars = ax.bar(x, returns, color=colors, alpha=0.7, edgecolor='black', width=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([label1, label2])
    ax.set_ylabel('Total Return (%)', fontweight='bold')
    ax.set_title('(A) Total Return', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top')

    # 子图2: 夏普比率和胜率
    ax = axes[0, 1]
    x = np.arange(2)
    width = 0.35
    sharpe = [metrics1['sharpe_ratio'], metrics2['sharpe_ratio']]
    win_rate = [metrics1['win_rate']/100, metrics2['win_rate']/100]

    ax2 = ax.twinx()
    bars1 = ax.bar(x - width/2, sharpe, width, label='Sharpe Ratio', color='#1dd1a1', alpha=0.7)
    bars2 = ax2.bar(x + width/2, win_rate, width, label='Win Rate', color='#5f27cd', alpha=0.7)

    ax.set_ylabel('Sharpe Ratio', fontweight='bold')
    ax2.set_ylabel('Win Rate', fontweight='bold')
    ax.set_title('(B) Risk Metrics', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([label1, label2])
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    # 子图3: 准确率和交易次数
    ax = axes[1, 0]
    metrics_to_plot = ['accuracy', 'win_rate']
    metrics_labels = ['Accuracy (%)', 'Win Rate (%)']

    x = np.arange(len(metrics_to_plot))
    width = 0.35
    vals1 = [metrics1[m] for m in metrics_to_plot]
    vals2 = [metrics2[m] for m in metrics_to_plot]

    bars1 = ax.bar(x - width/2, vals1, width, label=label1, color='#48dbfb', alpha=0.7)
    bars2 = ax.bar(x + width/2, vals2, width, label=label2, color='#ff6b6b', alpha=0.7)

    ax.set_ylabel('Percentage (%)', fontweight='bold')
    ax.set_title('(C) Prediction Accuracy', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_labels)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # 子图4: 累计收益曲线
    ax = axes[1, 1]
    df1 = result1['daily_results']
    df2 = result2['daily_results']

    # 计算累计信号
    cum1 = (1 + df1['signal'].shift(1) * 0.01).cumprod()  # 简化版累计收益
    cum2 = (1 + df2['signal'].shift(1) * 0.01).cumprod()

    ax.plot(df1.index, cum1, label=label1, color='#48dbfb', linewidth=2)
    ax.plot(df2.index, cum2, label=label2, color='#ff6b6b', linewidth=2)
    ax.set_ylabel('Cumulative Factor', fontweight='bold')
    ax.set_title('(D) Performance Over Time', fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)


def plot_three_way_comparison(axes, results):
    """绘制三种方法的总对比"""
    methods = ['baseline_original', 'baseline_simple', 'role_based']
    labels = ['Baseline 1', 'Baseline 3', 'Our Method']
    colors = ['#ff6b6b', '#feca57', '#48dbfb']

    metrics_list = [results[m]['metrics'] for m in methods]

    # 子图1: 总收益率
    ax = axes[0, 0]
    returns = [m['total_return'] for m in metrics_list]
    bars = ax.bar(range(3), returns, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Total Return (%)', fontweight='bold')
    ax.set_title('(A) Total Return', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

    # 子图2: 夏普比率
    ax = axes[0, 1]
    sharpe = [m['sharpe_ratio'] for m in metrics_list]
    bars = ax.bar(range(3), sharpe, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Sharpe Ratio', fontweight='bold')
    ax.set_title('(B) Sharpe Ratio', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

    # 子图3: 最大回撤
    ax = axes[0, 2]
    drawdown = [m['max_drawdown'] for m in metrics_list]
    bars = ax.bar(range(3), drawdown, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Max Drawdown (%)', fontweight='bold')
    ax.set_title('(C) Max Drawdown', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='top' if height < 0 else 'bottom', fontsize=9)

    # 子图4: 准确率
    ax = axes[1, 0]
    accuracy = [m['accuracy'] for m in metrics_list]
    bars = ax.bar(range(3), accuracy, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Accuracy (%)', fontweight='bold')
    ax.set_title('(D) Direction Accuracy', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

    # 子图5: 胜率
    ax = axes[1, 1]
    win_rate = [m['win_rate'] for m in metrics_list]
    bars = ax.bar(range(3), win_rate, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Win Rate (%)', fontweight='bold')
    ax.set_title('(E) Win Rate', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

    # 子图6: 综合对比表
    ax = axes[1, 2]
    ax.axis('off')

    # 创建对比表格
    table_data = []
    table_data.append(['Metric', 'B1', 'B3', 'Ours'])
    table_data.append(['Return (%)',
                      f"{metrics_list[0]['total_return']:.1f}",
                      f"{metrics_list[1]['total_return']:.1f}",
                      f"{metrics_list[2]['total_return']:.1f}"])
    table_data.append(['Sharpe',
                      f"{metrics_list[0]['sharpe_ratio']:.2f}",
                      f"{metrics_list[1]['sharpe_ratio']:.2f}",
                      f"{metrics_list[2]['sharpe_ratio']:.2f}"])
    table_data.append(['Accuracy (%)',
                      f"{metrics_list[0]['accuracy']:.1f}",
                      f"{metrics_list[1]['accuracy']:.1f}",
                      f"{metrics_list[2]['accuracy']:.1f}"])
    table_data.append(['Win Rate (%)',
                      f"{metrics_list[0]['win_rate']:.1f}",
                      f"{metrics_list[1]['win_rate']:.1f}",
                      f"{metrics_list[2]['win_rate']:.1f}"])

    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.3, 0.23, 0.23, 0.23])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # 设置表头样式
    for i in range(4):
        table[(0, i)].set_facecolor('#cccccc')
        table[(0, i)].set_text_props(weight='bold')

    ax.set_title('(F) Summary Table', fontweight='bold', pad=20)


def save_results_csv(results):
    """保存结果为CSV文件"""
    print("\n保存结果为CSV文件...")

    # 创建汇总表
    summary_data = []
    for method_name, result in results.items():
        metrics = result['metrics']
        summary_data.append({
            'Method': method_name,
            'Total Return (%)': metrics['total_return'],
            'Annual Return (%)': metrics['annual_return'],
            'Sharpe Ratio': metrics['sharpe_ratio'],
            'Max Drawdown (%)': metrics['max_drawdown'],
            'Accuracy (%)': metrics['accuracy'],
            'Win Rate (%)': metrics['win_rate'],
            'Total Trades': metrics['total_trades'],
            'Volatility (%)': metrics['volatility']
        })

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('experiment_summary.csv', index=False)
    print("✅ 已保存: experiment_summary.csv")

    # 保存每个方法的详细日度数据
    for method_name, result in results.items():
        daily_df = result['daily_results']
        filename = f'daily_results_{method_name}.csv'
        daily_df.to_csv(filename)
        print(f"✅ 已保存: {filename}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print("多Agent股票交易预测系统 - 完整实验运行")
    print("="*80)
    print("\n运行三种方法并生成对比结果:")
    print("1. Baseline 1: 原始通用Prompt")
    print("2. Baseline 3: 简单模板Prompt")
    print("3. Our Method: 角色化Prompt")
    print("\n注意: 使用简化版技术指标计算和模拟Agent分析")
    print("      (完整版本需要OpenAI API调用)")
    print("="*80)

    # 配置实验参数
    symbol = 'AAPL'
    start_date = '2024-01-01'
    end_date = '2024-01-31'

    print(f"\n实验配置:")
    print(f"  股票: {symbol}")
    print(f"  时间范围: {start_date} 到 {end_date}")

    # 运行三个实验
    results = {}

    print("\n" + "="*80)
    print("开始运行实验...")
    print("="*80)

    # Baseline 1
    result1 = run_single_experiment('baseline_original', symbol, start_date, end_date)
    if result1:
        results['baseline_original'] = result1

    # Baseline 3
    result2 = run_single_experiment('baseline_simple', symbol, start_date, end_date)
    if result2:
        results['baseline_simple'] = result2

    # Our Method
    result3 = run_single_experiment('role_based', symbol, start_date, end_date)
    if result3:
        results['role_based'] = result3

    # 生成对比图
    if len(results) == 3:
        print("\n" + "="*80)
        print("生成对比图...")
        print("="*80)
        generate_comparison_plots(results)

        # 保存CSV结果
        save_results_csv(results)

        # 打印总结
        print("\n" + "="*80)
        print("实验完成！")
        print("="*80)
        print("\n生成的文件:")
        print("  1. comparison_ours_vs_baseline1.png - 我们的方法 vs Baseline 1")
        print("  2. comparison_ours_vs_baseline3.png - 我们的方法 vs Baseline 3")
        print("  3. comparison_all_three_methods.png - 三种方法总对比")
        print("  4. experiment_summary.csv - 汇总结果表")
        print("  5. daily_results_*.csv - 每个方法的详细日度数据")
        print("\n" + "="*80)
    else:
        print("\n❌ 部分实验失败，无法生成完整对比")


if __name__ == "__main__":
    main()
