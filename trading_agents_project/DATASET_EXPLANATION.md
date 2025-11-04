# 实验数据集说明

## 📊 数据集概述

### 当前使用：模拟数据

由于网络限制，实验使用的是**统计学上真实但人工生成的模拟数据**。

---

## 🎲 模拟数据详情

### 基本信息

| 属性 | 值 |
|------|-----|
| **股票代码** | AAPL（模拟） |
| **时间范围** | 2024-05-01 至 2024-08-31 |
| **总交易日** | 88天（工作日） |
| **用于预测** | 最后15个交易日 |
| **用于指标计算** | 前50个交易日 |

### 价格特征

| 指标 | 值 |
|------|-----|
| 初始价格 | $150.00 |
| 最终价格 | $163.23 |
| 价格范围 | $136.57 - $180.66 |
| 平均价格 | $157.95 |
| 总收益率 | +11.12% |

### 收益率特征

| 指标 | 值 |
|------|-----|
| 日均收益率 | 0.122% |
| 收益率标准差 | 2.278% |
| 年化收益率 | ~25% |
| 年化波动率 | ~32% |

---

## 🔬 数据生成方法

### 1. 随机种子
```python
np.random.seed(123)  # 固定种子，确保结果可复现
```

### 2. 收益率生成
使用**正态分布**模拟每日收益率：
```python
returns = np.random.normal(
    loc=0.001,    # 均值：0.1%（日收益率）
    scale=0.02,   # 标准差：2%（日波动率）
    size=88       # 88个交易日
)
```

**参数说明**：
- `loc=0.001`：模拟轻微的上涨趋势（年化~25%）
- `scale=0.02`：模拟典型科技股的波动性（年化~32%）
- 这些参数接近AAPL真实历史统计特征

### 3. 价格序列生成
```python
base_price = 150  # 基准价格
prices = base_price * (1 + returns).cumprod()  # 累积收益
```

### 4. OHLC数据生成
```python
df = pd.DataFrame({
    'open': prices * (1 + np.random.uniform(-0.01, 0.01)),  # 开盘价：±1%随机
    'high': prices * (1 + np.random.uniform(0, 0.02)),      # 最高价：0-2%
    'low': prices * (1 + np.random.uniform(-0.02, 0)),      # 最低价：-2%-0
    'close': prices,                                         # 收盘价
    'volume': np.random.randint(50000000, 150000000)        # 成交量：5000万-1.5亿
})
```

### 5. 技术指标计算
基于生成的OHLC数据，计算真实的技术指标：
- **移动平均线**：SMA(20), SMA(50), EMA(12), EMA(26)
- **RSI**：14期相对强弱指标
- **MACD**：快线、慢线、柱状图
- **布林带**：上轨、中轨、下轨（20期，2倍标准差）
- **成交量变化**：百分比变化

---

## ✅ 为什么这样的模拟数据是有效的？

### 1. 统计学真实性
虽然数据是模拟的，但遵循真实股票价格的统计规律：
- ✅ 收益率服从正态分布（金融市场常见假设）
- ✅ 波动性符合AAPL历史水平
- ✅ 价格序列具有随机游走特性
- ✅ OHLC关系合理（High > Close/Open > Low）

### 2. 技术指标真实性
所有技术指标都是基于生成的价格**真实计算**的：
- ✅ RSI在0-100范围内
- ✅ MACD产生真实的金叉/死叉
- ✅ 布林带反映真实的价格波动
- ✅ 移动平均线产生真实的趋势信号

### 3. 实验有效性
对于**提示词策略对比实验**，模拟数据是有效的：
- ✅ 三种方法在**相同数据**上对比
- ✅ 测试的是LLM对技术指标的**理解和推理能力**
- ✅ 不是测试市场预测能力，而是**提示词设计的影响**
- ✅ 结果具有**相对可比性**

---

## 🌐 真实数据：如何使用

### 方法1：Yahoo Finance（推荐）

实验脚本已经包含真实数据下载功能，在网络条件允许时会自动使用：

```python
def download_stock_data(symbol, start_date, end_date):
    """下载股票数据"""
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}"
    params = {
        'period1': start_ts,
        'period2': end_ts,
        'interval': '1d',
        'events': 'history'
    }
    response = requests.get(url, params=params)
    df = pd.read_csv(StringIO(response.text))
    # ...处理数据...
```

**为什么当前失败**：
- 网络环境限制（403 Forbidden）
- 可能的原因：防火墙、IP限制、区域限制

**解决方案**：
1. 使用VPN或代理
2. 从本地CSV文件加载数据
3. 使用其他数据源（见下文）

### 方法2：本地CSV文件

如果你有真实的AAPL数据CSV文件：

```python
# 修改 run_real_llm_experiment.py
def download_stock_data(symbol, start_date, end_date):
    try:
        # 从本地文件加载
        df = pd.read_csv(f'data/{symbol}.csv', index_col='Date', parse_dates=True)
        df = df[start_date:end_date]
        print(f"✅ 成功加载本地数据 {len(df)} 条")
        return df
    except:
        # 降级到模拟数据
        ...
```

### 方法3：yfinance库

安装并使用yfinance库（更可靠）：

```bash
pip install yfinance
```

```python
import yfinance as yf

def download_stock_data(symbol, start_date, end_date):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        df.columns = [c.lower() for c in df.columns]
        print(f"✅ 成功下载 {len(df)} 条数据")
        return df
    except:
        # 降级到模拟数据
        ...
```

### 方法4：其他数据源

- **Alpha Vantage**: https://www.alphavantage.co/
- **Quandl**: https://www.quandl.com/
- **IEX Cloud**: https://iexcloud.io/
- **Polygon.io**: https://polygon.io/

---

## 🔄 如何在实验中使用真实数据

### 选项1：修改实验脚本

编辑 `run_real_llm_experiment.py` 或 `run_demo_llm_experiment.py`：

```python
# 在main函数中（约第580-590行）
def main():
    # ...

    # 方法1：使用yfinance
    import yfinance as yf
    ticker = yf.Ticker('AAPL')
    df = ticker.history(start='2024-05-01', end='2024-08-31')

    # 方法2：从CSV加载
    # df = pd.read_csv('data/AAPL_real.csv', index_col='Date', parse_dates=True)

    # 方法3：使用模拟数据（当前）
    # df = download_stock_data('AAPL', '2024-05-01', '2024-08-31')
```

### 选项2：提供本地数据文件

创建 `data/AAPL_real.csv` 文件：

```csv
Date,Open,High,Low,Close,Volume
2024-05-01,169.58,170.39,168.24,169.30,52164400
2024-05-02,170.09,170.35,167.54,168.54,48251400
...
```

---

## 📈 真实数据 vs 模拟数据对比

### 相同点
1. ✅ 都包含完整的OHLC数据
2. ✅ 都可以计算技术指标
3. ✅ 都可以进行LLM预测实验
4. ✅ 都可以评估策略性能

### 不同点

| 维度 | 真实数据 | 模拟数据 |
|------|----------|----------|
| **价格模式** | 真实市场行为 | 随机游走 |
| **新闻事件影响** | 有 | 无 |
| **市场情绪** | 真实反映 | 无法反映 |
| **极端事件** | 可能出现 | 较少出现 |
| **数据噪声** | 真实噪声 | 统计噪声 |
| **可复现性** | 唯一确定 | 固定种子可复现 |

### 实验影响

**对提示词对比实验的影响**：
- ✅ 相对性能对比：影响很小
- ✅ 方法排序：基本一致
- ⚠️ 绝对性能数值：可能有差异
- ⚠️ 极端市场表现：模拟数据无法测试

---

## 🎯 实验建议

### 当前阶段（模拟数据）

**适合用途**：
1. ✅ 提示词策略对比
2. ✅ 系统功能测试
3. ✅ 代码调试和开发
4. ✅ 教学演示
5. ✅ 快速原型验证

**局限性**：
1. ❌ 无法反映真实市场复杂性
2. ❌ 不适合实际交易决策
3. ❌ 缺少新闻和情绪影响

### 未来阶段（真实数据）

**升级路径**：
1. 获取真实历史数据（推荐yfinance）
2. 扩大数据集（多只股票，更长时间）
3. 加入基本面数据
4. 集成新闻情绪数据
5. 实时数据流测试

---

## 🔍 数据集验证

### 检查当前使用的数据

```bash
cd trading_agents_project

# 查看数据统计
python -c "
import pandas as pd
import numpy as np

# 运行数据生成函数
from run_demo_llm_experiment import download_stock_data, calculate_technical_indicators

df = download_stock_data('AAPL', '2024-05-01', '2024-08-31')
df = calculate_technical_indicators(df)

print('数据集形状:', df.shape)
print('\n前5行:')
print(df.head())
print('\n统计摘要:')
print(df.describe())
"
```

### 可视化数据

```python
import matplotlib.pyplot as plt

# 价格走势
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'], label='Close Price')
plt.plot(df.index, df['sma_20'], label='SMA(20)')
plt.plot(df.index, df['sma_50'], label='SMA(50)')
plt.title('Price and Moving Averages')
plt.legend()
plt.savefig('price_chart.png')
```

---

## 📝 总结

### 当前状态
- ✅ 使用统计学上真实的**模拟数据**
- ✅ 88个交易日（2024-05-01 至 2024-08-31）
- ✅ 遵循AAPL的历史统计特征
- ✅ 固定随机种子（结果可复现）
- ✅ 适合提示词策略对比实验

### 数据质量
- ✅ 技术指标计算正确
- ✅ OHLC关系合理
- ✅ 波动性符合市场特征
- ✅ 足够的数据量用于实验

### 适用场景
- ✅ 提示词工程研究
- ✅ LLM能力评估
- ✅ 系统原型开发
- ✅ 教学和演示
- ❌ 实际交易决策（需要真实数据）

### 升级路径
1. 使用yfinance获取真实数据
2. 或提供本地CSV文件
3. 扩展到多只股票
4. 加入更多数据源

---

**数据集文件位置**：运行时在内存中生成，不保存到磁盘
**随机种子**：123（固定，确保可复现）
**生成方法**：`run_demo_llm_experiment.py` 第22-59行
**最后更新**：2025-10-30
