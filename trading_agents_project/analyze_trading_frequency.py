#!/usr/bin/env python3
"""
分析交易结果中的交易次数
根据配置的日期范围和交易策略，计算实际的交易次数
"""

from datetime import datetime, timedelta

def calculate_trading_days(start_date_str="2022-01-01", end_date_str="2024-10-01"):
    """计算配置的日期范围内有多少个交易日"""
    # 解析日期
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # 计算工作日（周一到周五）
    current_date = start_date
    trading_days = 0

    while current_date <= end_date:
        # 0 = Monday, 6 = Sunday
        if current_date.weekday() < 5:  # Monday to Friday
            trading_days += 1
        current_date += timedelta(days=1)

    return trading_days

def estimate_trade_counts_by_strategy():
    """根据不同策略估算交易次数"""

    start_date = "2022-01-01"
    end_date = "2024-10-01"
    total_days = calculate_trading_days(start_date, end_date)

    print("=" * 70)
    print("交易次数分析")
    print("=" * 70)
    print(f"\n数据时间范围: {start_date} 至 {end_date}")
    print(f"总交易日数量: {total_days} 天")
    print()

    # 根据图片中的三种方法估算交易频率
    strategies = {
        "方法1 (Accuracy=39.1%, Sharpe=-3.5, WinRate=47.6%)": {
            "description": "基准方法1 - 可能是随机或低频策略",
            "estimated_trade_frequency": 0.15,  # 约15%的天数产生交易
        },
        "方法2 (Accuracy=39.1%, Sharpe=1.0, WinRate=47.6%)": {
            "description": "基准方法2 - 改进的基准策略",
            "estimated_trade_frequency": 0.20,  # 约20%的天数产生交易
        },
        "方法3 (Accuracy=47.8%, Sharpe=8.0, WinRate=76.2%)": {
            "description": "最优方法 - 多Agent角色定制化Prompt",
            "estimated_trade_frequency": 0.25,  # 约25%的天数产生交易
        }
    }

    print("各策略估算的交易次数:")
    print("-" * 70)

    for strategy_name, info in strategies.items():
        estimated_trades = int(total_days * info["estimated_trade_frequency"])
        print(f"\n{strategy_name}")
        print(f"  描述: {info['description']}")
        print(f"  预估交易频率: {info['estimated_trade_frequency']*100:.1f}%")
        print(f"  预估交易次数: {estimated_trades} 次")
        print(f"  平均持仓天数: {total_days / estimated_trades:.1f} 天")

    print("\n" + "=" * 70)
    print("说明:")
    print("=" * 70)
    print("""
1. 实际交易次数取决于策略产生的非零信号数量
2. 上述估算基于常见交易策略的频率范围
3. 高Sharpe比率(8.0)和高胜率(76.2%)的方法3可能采用更保守、更精确的交易时机选择
4. 负Sharpe比率(-3.5)的方法1可能存在过度交易或时机选择不当的问题
5. 要获取准确的交易次数，需要运行完整实验并查看 'total_trades' 指标

建议：
- 运行实验脚本以获取精确的交易次数统计
- 检查 results/ 目录中的详细输出文件
- 查看每日交易信号的分布情况
    """)

def analyze_from_metrics():
    """基于典型的交易指标反推交易特征"""
    print("\n" + "=" * 70)
    print("基于指标的交易特征分析")
    print("=" * 70)

    total_days = calculate_trading_days("2022-01-01", "2024-10-01")

    # 基于图片中的三组数据
    methods = [
        {
            "name": "方法1",
            "accuracy": 0.391,
            "sharpe": -3.5,
            "win_rate": 0.476,
        },
        {
            "name": "方法2",
            "accuracy": 0.391,
            "sharpe": 1.0,
            "win_rate": 0.476,
        },
        {
            "name": "方法3",
            "accuracy": 0.478,
            "sharpe": 8.0,
            "win_rate": 0.762,
        }
    ]

    print(f"\n假设测试期间总交易日: {total_days} 天")
    print("\n不同持仓比例下的预估交易次数:")
    print("-" * 70)

    for method in methods:
        print(f"\n{method['name']}:")
        print(f"  准确率: {method['accuracy']*100:.1f}%")
        print(f"  夏普比率: {method['sharpe']:.1f}")
        print(f"  胜率: {method['win_rate']*100:.1f}%")
        print(f"\n  如果持仓率为:")

        for hold_ratio in [0.10, 0.15, 0.20, 0.25, 0.30]:
            trades = int(total_days * hold_ratio)
            winning_trades = int(trades * method['win_rate'])
            losing_trades = trades - winning_trades

            print(f"    {hold_ratio*100:.0f}% → 约 {trades:3d} 次交易 "
                  f"(盈利: {winning_trades:3d}, 亏损: {losing_trades:3d})")

if __name__ == "__main__":
    estimate_trade_counts_by_strategy()
    analyze_from_metrics()
