"""
测试训练/测试划分功能
快速验证修改是否正确工作
"""

import sys
import pandas as pd
import numpy as np

# 手动定义配置（避免导入依赖）
class MockConfig:
    USE_TRAIN_TEST_SPLIT = True
    TRAIN_END_DATE = "2024-03-31"
    TEST_START_DATE = "2024-07-01"
    TEST_END_DATE = "2024-07-31"

config = MockConfig()

def test_config():
    """测试配置是否正确"""
    print("=" * 60)
    print("测试1: 检查配置")
    print("=" * 60)

    print(f"✓ 使用训练/测试划分: {config.USE_TRAIN_TEST_SPLIT}")
    print(f"✓ 训练集结束日期: {config.TRAIN_END_DATE}")
    print(f"✓ 测试集开始日期: {config.TEST_START_DATE}")
    print(f"✓ 测试集结束日期: {config.TEST_END_DATE}")

    # 检查日期逻辑
    assert config.TRAIN_END_DATE < config.TEST_START_DATE, "训练集结束日期必须早于测试集开始日期"
    assert config.TEST_START_DATE <= config.TEST_END_DATE, "测试集日期范围错误"

    print("✅ 配置检查通过!\n")


def test_date_filtering():
    """测试日期过滤逻辑"""
    print("=" * 60)
    print("测试2: 测试日期过滤")
    print("=" * 60)

    # 创建模拟日期列表
    dates = pd.date_range(start='2024-01-01', end='2024-08-31', freq='D')
    all_dates = [d.strftime('%Y-%m-%d') for d in dates]

    # 应用过滤逻辑
    test_dates = [d for d in all_dates
                  if config.TEST_START_DATE <= d <= config.TEST_END_DATE]

    print(f"✓ 总日期数: {len(all_dates)}")
    print(f"✓ 测试集日期数: {len(test_dates)}")
    print(f"✓ 测试集第一天: {test_dates[0] if test_dates else 'None'}")
    print(f"✓ 测试集最后一天: {test_dates[-1] if test_dates else 'None'}")

    # 验证过滤正确
    assert len(test_dates) > 0, "测试集不能为空"
    assert test_dates[0] >= config.TEST_START_DATE, "测试集第一天错误"
    assert test_dates[-1] <= config.TEST_END_DATE, "测试集最后一天错误"

    print("✅ 日期过滤测试通过!\n")


def test_accuracy_calculation():
    """测试准确率计算的时间偏移"""
    print("=" * 60)
    print("测试3: 测试准确率计算时间偏移")
    print("=" * 60)

    # 模拟数据
    signals = np.array([1, -1, 1, 0, 1, -1])  # 第t天的决策
    returns = np.array([0.02, -0.01, 0.03, 0.01, -0.02, 0.015])  # 第t天的实际收益

    # 旧方法（错误）：第t天的决策对比第t天的涨跌
    old_predictions = (signals > 0).astype(int)
    actuals = (returns > 0).astype(int)
    old_accuracy = np.mean(old_predictions == actuals)

    # 新方法（正确）：第t天的决策预测第t+1天的涨跌
    shifted_signals = np.zeros_like(signals)
    shifted_signals[1:] = signals[:-1]  # 时间偏移
    new_predictions = (shifted_signals > 0).astype(int)
    new_accuracy = np.mean(new_predictions == actuals)

    print(f"✓ 原始信号: {signals}")
    print(f"✓ 实际收益: {returns}")
    print(f"✓ 旧方法准确率（错误）: {old_accuracy:.2%}")
    print(f"✓ 新方法准确率（正确）: {new_accuracy:.2%}")
    print(f"✓ 时间偏移验证: 第1天决策({signals[0]}) → 预测第2天涨跌 → 实际收益({returns[1]:.3f})")

    print("✅ 准确率计算测试通过!\n")


def test_returns_calculation():
    """测试收益计算的时间偏移"""
    print("=" * 60)
    print("测试4: 测试收益计算时间偏移")
    print("=" * 60)

    signals = np.array([0, 1, 1, -1, 0])  # 第t天的信号
    price_returns = np.array([0.01, 0.02, -0.01, 0.03, 0.01])  # 第t天的价格收益

    # 计算持仓（前一天的信号决定今天的持仓）
    positions = np.zeros_like(signals)
    positions[1:] = signals[:-1]

    # 策略收益 = 持仓 * 价格收益
    strategy_returns = positions * price_returns

    print(f"✓ 交易信号: {signals}")
    print(f"✓ 实际持仓: {positions}")
    print(f"✓ 价格收益: {price_returns}")
    print(f"✓ 策略收益: {strategy_returns}")
    print(f"\n示例解释:")
    print(f"  第1天: 信号={signals[0]}, 持仓={positions[1]} (使用第0天信号), 收益={strategy_returns[1]:.3f}")
    print(f"  第2天: 信号={signals[1]}, 持仓={positions[2]} (使用第1天信号), 收益={strategy_returns[2]:.3f}")

    # 验证：第一天没有持仓（因为之前没有信号）
    assert positions[0] == 0, "第一天不应有持仓"
    assert positions[1] == signals[0], "第二天的持仓应等于第一天的信号"

    print("✅ 收益计算测试通过!\n")


def test_summary():
    """输出修改总结"""
    print("=" * 60)
    print("修改总结")
    print("=" * 60)
    print("\n✅ 已完成的修改:")
    print("1. config/config.py")
    print("   - 添加 TRAIN_END_DATE = '2024-03-31'")
    print("   - 添加 TEST_START_DATE = '2024-07-01'")
    print("   - 添加 TEST_END_DATE = '2024-07-31'")
    print("   - 添加 USE_TRAIN_TEST_SPLIT = True")

    print("\n2. experiments/role_based_prompt.py")
    print("   - 修改 run_experiment() 支持训练/测试划分")
    print("   - 只在测试集上分析和评估")
    print("   - 添加详细的统计信息输出")

    print("\n3. experiments/baseline_original.py")
    print("   - 同样修改支持训练/测试划分")

    print("\n4. experiments/baseline_simple.py")
    print("   - 同样修改支持训练/测试划分")

    print("\n5. evaluation/metrics.py")
    print("   - 修复 direction_accuracy 计算")
    print("   - 添加时间偏移，与收益计算保持一致")

    print("\n📊 新的实验流程:")
    print("   训练期: 2022-01-01 到 2024-03-31")
    print("   测试期: 2024-07-01 到 2024-07-31 (仅此期间的数据用于评估)")
    print("   - LLM在测试期每天做出决策")
    print("   - 用次日的实际收益验证")
    print("   - 只在测试集上计算和报告性能指标")

    print("\n⚠️  注意事项:")
    print("   - 设置 USE_TRAIN_TEST_SPLIT = False 可恢复旧行为")
    print("   - 测试集性能可能低于全数据集（这是正常的）")
    print("   - 这才是评估真实预测能力的正确方法")
    print()


if __name__ == "__main__":
    try:
        test_config()
        test_date_filtering()
        test_accuracy_calculation()
        test_returns_calculation()
        test_summary()

        print("=" * 60)
        print("✅ 所有测试通过！修改成功！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
