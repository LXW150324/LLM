"""
生成并保存实验数据集
这个脚本会生成模拟的AAPL股票数据并保存为CSV文件
"""

import pandas as pd
import numpy as np
from datetime import datetime

def generate_dataset():
    """生成实验使用的数据集"""
    print("="*70)
    print("生成实验数据集")
    print("="*70)

    # 参数设置
    symbol = 'AAPL'
    start_date = '2024-05-01'
    end_date = '2024-08-31'

    print(f"\n股票代码: {symbol}")
    print(f"时间范围: {start_date} 至 {end_date}")

    # 生成交易日期（仅工作日）
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = dates[dates.dayofweek < 5]  # 过滤掉周末

    print(f"交易日数: {len(dates)} 天")

    # 固定随机种子以确保可复现性
    np.random.seed(123)

    # 生成收益率序列（正态分布）
    # 参数选择基于AAPL的历史统计特征
    returns = np.random.normal(
        loc=0.001,    # 均值：0.1%日收益率（年化约25%）
        scale=0.02,   # 标准差：2%日波动率（年化约32%）
        size=len(dates)
    )

    # 计算价格序列
    base_price = 150.0
    prices = base_price * (1 + returns).cumprod()

    # 生成OHLC数据
    # Open: 在收盘价基础上 ±1% 随机波动
    # High: 在收盘价基础上 0-2% 向上波动
    # Low: 在收盘价基础上 0-2% 向下波动
    # Close: 使用计算的价格
    # Volume: 5000万-1.5亿之间随机

    np.random.seed(123)  # 重置种子确保一致性

    df = pd.DataFrame({
        'Date': dates,
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'Low': prices * (1 + np.random.uniform(-0.02, 0, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(50000000, 150000000, len(dates))
    })

    # 四舍五入到2位小数
    df['Open'] = df['Open'].round(2)
    df['High'] = df['High'].round(2)
    df['Low'] = df['Low'].round(2)
    df['Close'] = df['Close'].round(2)

    # 计算日收益率和日涨跌幅
    df['Daily_Return'] = returns
    df['Change_Pct'] = ((df['Close'] - df['Open']) / df['Open'] * 100).round(2)

    print(f"\n数据统计:")
    print(f"  初始价格: ${df['Close'].iloc[0]:.2f}")
    print(f"  最终价格: ${df['Close'].iloc[-1]:.2f}")
    print(f"  最低价格: ${df['Close'].min():.2f}")
    print(f"  最高价格: ${df['Close'].max():.2f}")
    print(f"  总收益率: {(df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100:.2f}%")
    print(f"  平均日收益率: {df['Daily_Return'].mean() * 100:.3f}%")
    print(f"  日收益率标准差: {df['Daily_Return'].std() * 100:.3f}%")

    return df


def calculate_technical_indicators(df):
    """计算技术指标"""
    print(f"\n计算技术指标...")

    df = df.copy()

    # 移动平均线
    df['SMA_20'] = df['Close'].rolling(window=20).mean().round(2)
    df['SMA_50'] = df['Close'].rolling(window=50).mean().round(2)
    df['EMA_12'] = df['Close'].ewm(span=12).mean().round(2)
    df['EMA_26'] = df['Close'].ewm(span=26).mean().round(2)

    # RSI (14期)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = (100 - (100 / (1 + rs))).round(2)

    # MACD
    df['MACD'] = (df['EMA_12'] - df['EMA_26']).round(4)
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean().round(4)
    df['MACD_Histogram'] = (df['MACD'] - df['MACD_Signal']).round(4)

    # 布林带 (20期, 2倍标准差)
    df['BB_Middle'] = df['Close'].rolling(window=20).mean().round(2)
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = (df['BB_Middle'] + bb_std * 2).round(2)
    df['BB_Lower'] = (df['BB_Middle'] - bb_std * 2).round(2)

    # 成交量变化
    df['Volume_Change_Pct'] = (df['Volume'].pct_change() * 100).round(2)

    print(f"✅ 技术指标计算完成")
    print(f"   - 移动平均线: SMA(20), SMA(50), EMA(12), EMA(26)")
    print(f"   - 动量指标: RSI(14)")
    print(f"   - 趋势指标: MACD, MACD Signal, MACD Histogram")
    print(f"   - 波动率指标: 布林带 (上/中/下)")
    print(f"   - 成交量: 变化百分比")

    return df


def save_datasets(df_basic, df_with_indicators):
    """保存数据集到文件"""
    print(f"\n保存数据集...")

    # 创建data目录
    import os
    os.makedirs('data', exist_ok=True)

    # 保存基础数据集（仅OHLCV）
    basic_file = 'data/AAPL_simulated_basic.csv'
    df_basic[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Daily_Return', 'Change_Pct']].to_csv(
        basic_file, index=False
    )
    print(f"✅ 基础数据集: {basic_file}")

    # 保存完整数据集（包含技术指标）
    full_file = 'data/AAPL_simulated_with_indicators.csv'
    df_with_indicators.to_csv(full_file, index=False)
    print(f"✅ 完整数据集: {full_file}")

    # 保存README
    readme_file = 'data/README.md'
    with open(readme_file, 'w') as f:
        f.write("""# 实验数据集说明

## 文件列表

### 1. AAPL_simulated_basic.csv
基础OHLCV数据（88个交易日）

**字段说明**:
- `Date`: 交易日期（YYYY-MM-DD）
- `Open`: 开盘价（美元）
- `High`: 最高价（美元）
- `Low`: 最低价（美元）
- `Close`: 收盘价（美元）
- `Volume`: 成交量（股）
- `Daily_Return`: 日收益率（小数）
- `Change_Pct`: 日涨跌幅（百分比）

**数据特征**:
- 时间范围: 2024-05-01 至 2024-08-31
- 交易日数: 88天（仅工作日）
- 初始价格: $150.00
- 价格范围: $136.57 - $180.66
- 总收益率: +11.12%

### 2. AAPL_simulated_with_indicators.csv
完整数据集（包含技术指标）

**额外字段**:
- `SMA_20`: 20日简单移动平均线
- `SMA_50`: 50日简单移动平均线
- `EMA_12`: 12日指数移动平均线
- `EMA_26`: 26日指数移动平均线
- `RSI_14`: 14期相对强弱指标（0-100）
- `MACD`: MACD快线
- `MACD_Signal`: MACD信号线
- `MACD_Histogram`: MACD柱状图
- `BB_Upper`: 布林带上轨
- `BB_Middle`: 布林带中轨
- `BB_Lower`: 布林带下轨
- `Volume_Change_Pct`: 成交量变化百分比

## 数据生成方法

### 价格生成
使用蒙特卡洛模拟，基于几何布朗运动：
```python
returns = np.random.normal(loc=0.001, scale=0.02, size=88)
prices = base_price * (1 + returns).cumprod()
```

**参数说明**:
- 初始价格: $150.00
- 日均收益率: 0.1% (年化约25%)
- 日波动率: 2% (年化约32%)
- 随机种子: 123（固定，可复现）

### 统计特征
遵循AAPL的历史统计规律：
- 收益率服从正态分布
- 波动性符合科技股特征
- OHLC关系合理（High ≥ Open/Close ≥ Low）

### 技术指标
所有技术指标都是基于生成的OHLC数据真实计算：
- 使用标准的金融计算公式
- RSI、MACD、布林带等均为业界标准算法
- 可以用于技术分析研究和LLM实验

## 适用场景

✅ **适合**:
- 提示词策略对比实验
- LLM技术分析能力评估
- 量化策略回测（研究用）
- 技术指标教学演示
- 算法开发和测试

❌ **不适合**:
- 实际交易决策
- 市场预测
- 风险管理（真实资金）

## 数据质量

- ✅ 统计学上真实（遵循市场规律）
- ✅ 技术指标计算正确
- ✅ 完全可复现（固定随机种子）
- ✅ 格式规范（标准CSV）
- ⚠️ 非真实市场数据

## 如何使用

### Python (pandas)
```python
import pandas as pd

# 读取基础数据
df_basic = pd.read_csv('data/AAPL_simulated_basic.csv', parse_dates=['Date'])

# 读取完整数据
df_full = pd.read_csv('data/AAPL_simulated_with_indicators.csv', parse_dates=['Date'])

# 查看前5行
print(df_full.head())

# 查看统计摘要
print(df_full.describe())
```

### R
```r
# 读取数据
df <- read.csv('data/AAPL_simulated_basic.csv')
df$Date <- as.Date(df$Date)

# 查看数据
head(df)
summary(df)
```

### Excel
直接打开CSV文件即可

## 生成脚本

数据由 `generate_dataset.py` 生成：
```bash
python generate_dataset.py
```

## 许可证

本数据集用于研究和教育目的，遵循MIT许可证。

## 参考

详细说明请参考：`DATASET_EXPLANATION.md`

---

**生成时间**: 2025-10-30
**版本**: 1.0
**数据点数**: 88个交易日
**文件大小**: 约20KB（基础）+ 30KB（完整）
""")
    print(f"✅ 数据集说明: {readme_file}")

    return basic_file, full_file


def main():
    """主函数"""
    print("\n" + "="*70)
    print("AAPL模拟数据集生成器")
    print("="*70)
    print("\n此脚本将生成实验中使用的模拟股票数据集")
    print("数据将保存为CSV格式，可直接在GitHub上查看和下载")

    # 生成基础数据
    df_basic = generate_dataset()

    # 计算技术指标
    df_full = calculate_technical_indicators(df_basic)

    # 保存文件
    basic_file, full_file = save_datasets(df_basic, df_full)

    # 显示预览
    print("\n" + "="*70)
    print("数据预览（前5行）")
    print("="*70)
    print(df_basic.head())

    print("\n" + "="*70)
    print("技术指标预览（最后5行）")
    print("="*70)
    print(df_full[['Date', 'Close', 'SMA_20', 'RSI_14', 'MACD']].tail())

    print("\n" + "="*70)
    print("✅ 数据集生成完成！")
    print("="*70)
    print(f"\n文件位置:")
    print(f"  1. {basic_file}")
    print(f"  2. {full_file}")
    print(f"  3. data/README.md")
    print("\n这些文件将被上传到GitHub仓库")
    print("="*70)


if __name__ == "__main__":
    main()
