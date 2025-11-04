# 实验数据集说明

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
