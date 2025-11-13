# 论文附录：三种提示词策略完整文本

## 研究设计说明

本研究对比了三种不同复杂度的提示词策略在股票交易预测任务中的表现。所有方法均使用相同的输入数据和评估标准，唯一变量为系统提示词（system prompt）的设计。

---

## 方法一：Baseline 1 - 通用提示词（Generic Prompt）

### 设计理念
最简化的提示词设计，仅包含任务描述和基本输出要求，不提供角色定义或专业指导。作为对照组基准。

### 完整提示词文本

```
You are a stock market analyst. Analyze the given stock data and provide a trading recommendation.

Output your analysis as JSON with these fields:
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "brief explanation"
}
```

### 字符数统计
- 总字符数：173
- 总词数：30

### 设计特征
- ✓ 简单直接的任务定义
- ✓ 结构化输出要求
- ✗ 无专业角色定义
- ✗ 无方法论指导
- ✗ 无工具清单
- ✗ 无专业注意事项

---

## 方法二：Baseline 3 - 简单角色定义（Simple Role-Based Prompt）

### 设计理念
引入角色定义和基本职责描述，提供初步的专业方向指导，但缺乏详细的方法论和工具说明。

### 完整提示词文本

```
You are a Technical Analyst specializing in stock market analysis.

Your role:
- Analyze price trends and technical indicators
- Provide buy/sell/hold recommendations
- Assess market conditions

Output your analysis as JSON with these fields:
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "your analysis"
}
```

### 字符数统计
- 总字符数：317
- 总词数：50

### 设计特征
- ✓ 明确的专业角色（Technical Analyst）
- ✓ 基本职责清单（3项）
- ✓ 结构化输出要求
- ✗ 缺少具体分析工具
- ✗ 缺少方法论指导
- ✗ 缺少专业注意事项

### 相比Baseline 1的改进
- 增加了角色定义（"Technical Analyst specializing in stock market analysis"）
- 明确了三项基本职责
- 字符数增加83%（173→317）

---

## 方法三：Our Method - 详细角色定义提示词（Detailed Role-Based Prompt）

### 设计理念
全面的专业角色构建，包含详细的职责描述、工具清单、输出规范和专业最佳实践指导。模拟真实技术分析师的思维框架。

### 完整提示词文本

```
You are an experienced Technical Analyst specializing in price trends and technical indicators.

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
- Base your analysis only on the provided technical data
```

### 字符数统计
- 总字符数：1,026
- 总词数：156

### 设计特征
- ✓ 详细的专业角色（"experienced Technical Analyst"）
- ✓ 明确的职责清单（4项具体任务）
- ✓ 工具分类清单（4类技术指标）
- ✓ 扩展的结构化输出（6个字段）
- ✓ 专业最佳实践（4条注意事项）
- ✓ 多指标交叉验证指导
- ✓ 专业术语使用（divergence, volume confirmation等）

### 相比Baseline 3的改进
1. **角色深化**："Technical Analyst" → "experienced Technical Analyst specializing in..."
2. **职责细化**：3项笼统职责 → 4项具体可执行任务
3. **工具清单**：无 → 4类技术分析工具及具体示例
4. **输出丰富**：3个基础字段 → 6个详细字段（增加趋势方向、强度、关键信号）
5. **专业指导**：无 → 4条最佳实践注意事项
6. **字符数**：增加224%（317→1,026）

---

## 输入数据格式（所有方法通用）

为确保公平对比，三种方法接收完全相同的市场数据输入：

```
Analyze the following technical data for AAPL:

Price Information:
- Current Price: $XXX.XX
- Open: $XXX.XX
- High: $XXX.XX
- Low: $XXX.XX
- Change: +X.XX%
- Volume: XXX,XXX,XXX

Trend Indicators:
- 20-day SMA: $XXX.XX
- 50-day SMA: $XXX.XX
- EMA12: $XXX.XX
- EMA26: $XXX.XX

Momentum Indicators:
- RSI(14): XX.XX
- MACD: X.XXXX
- MACD Signal: X.XXXX
- MACD Histogram: X.XXXX

Volatility Indicators:
- Bollinger Upper: $XXX.XX
- Bollinger Middle: $XXX.XX
- Bollinger Lower: $XXX.XX

Volume:
- Volume Change: +X.XX%

Please provide your trading recommendation based on this technical data.
```

---

## 提示词设计维度对比

| 设计维度 | Baseline 1 | Baseline 3 | Our Method |
|---------|-----------|-----------|------------|
| **角色定义** | 简单（"stock market analyst"） | 中等（"Technical Analyst"） | 详细（"experienced Technical Analyst specializing..."） |
| **职责描述** | 无 | 3项笼统 | 4项具体 |
| **工具清单** | 无 | 无 | 4类共8项 |
| **输出字段数** | 3个 | 3个 | 6个 |
| **专业指导** | 无 | 无 | 4条 |
| **字符数** | 173 | 317 | 1,026 |
| **词数** | 30 | 50 | 156 |
| **复杂度** | 低 | 中 | 高 |

---

## 提示词工程关键差异点

### 1. 角色构建（Role Construction）

**Baseline 1**:
- 角色：stock market analyst（泛化角色）
- 专业性：低

**Baseline 3**:
- 角色：Technical Analyst specializing in stock market analysis
- 专业性：中
- 改进：明确了技术分析专业方向

**Our Method**:
- 角色：experienced Technical Analyst specializing in price trends and technical indicators
- 专业性：高
- 改进：
  - 强调经验（"experienced"）
  - 双重专业化（price trends + technical indicators）
  - 建立专家身份

### 2. 任务框架（Task Framework）

**Baseline 1**:
- 任务：Analyze... and provide recommendation（单一任务）

**Baseline 3**:
- 任务：3项笼统职责
  - Analyze price trends and technical indicators
  - Provide buy/sell/hold recommendations
  - Assess market conditions

**Our Method**:
- 任务：4项具体可执行职责
  - Analyze price trends (uptrend/downtrend/sideways) ← 提供具体分类
  - Interpret technical indicators (RSI, MACD, Bollinger Bands, etc.) ← 列举具体工具
  - Identify key support and resistance levels ← 技术分析核心概念
  - Evaluate the strength of buy/sell signals ← 信号强度评估

**改进**: 从笼统到具体，从任务到可执行步骤

### 3. 工具赋能（Tool Specification）

**Baseline 1 & 3**:
- 工具说明：无

**Our Method**:
- 工具分类：
  - Trend indicators: Moving averages, MACD
  - Momentum indicators: RSI
  - Volatility indicators: Bollinger Bands
  - Volume indicators

**意义**:
- 明确分析框架
- 提供工具箱清单
- 引导系统化分析

### 4. 输出结构（Output Structure）

**Baseline 1 & 3**:
```json
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "..."
}
```
- 3个基础字段
- 仅提供结论和置信度

**Our Method**:
```json
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "trend_direction": "uptrend/downtrend/sideways",
    "trend_strength": "strong/moderate/weak",
    "key_signals": ["..."],
    "reasoning": "detailed technical analysis reasoning"
}
```
- 6个详细字段
- 包含趋势方向、强度
- 要求列举关键信号
- 强调详细推理

**改进**:
- 更丰富的分析维度
- 可解释性增强
- 强制系统化思考

### 5. 专业指导（Professional Guidelines）

**Baseline 1 & 3**:
- 专业指导：无

**Our Method**:
- 4条最佳实践：
  1. Signals are more reliable when multiple indicators confirm each other
     （多指标交叉验证）
  2. Pay attention to divergence (price vs indicator inconsistency)
     （关注背离现象）
  3. Consider volume confirmation
     （考虑成交量确认）
  4. Base your analysis only on the provided technical data
     （仅基于提供数据）

**意义**:
- 引入专业知识
- 提供分析范式
- 避免常见错误
- 提高预测质量

---

## 提示词长度与复杂度分析

| 指标 | Baseline 1 | Baseline 3 | Our Method | B3/B1 | OM/B3 |
|------|-----------|-----------|------------|-------|-------|
| 字符数 | 173 | 317 | 1,026 | +83% | +224% |
| 词数 | 30 | 50 | 156 | +67% | +212% |
| 句子数 | 3 | 6 | 15 | +100% | +150% |
| 结构层次 | 1层 | 2层 | 4层 | - | - |
| 关键概念数 | 3 | 6 | 18 | +100% | +200% |

**说明**:
- 结构层次：Baseline 1（任务）→ Baseline 3（角色+任务）→ Our Method（角色+职责+工具+输出+指导）
- 关键概念：包括角色、职责、工具、指标等专业术语

---

## 理论基础与设计原则

### 提示词工程维度（Prompt Engineering Dimensions）

本研究基于以下提示词工程理论框架：

1. **角色设定（Role Assignment）**
   - 理论：给LLM赋予特定角色可激活相关知识域
   - 实践：Baseline 1（无）→ Baseline 3（简单）→ Our Method（详细）

2. **任务分解（Task Decomposition）**
   - 理论：将复杂任务分解为可执行子任务
   - 实践：Our Method 将"分析"分解为4个具体步骤

3. **上下文赋能（Context Enrichment）**
   - 理论：提供工具、知识、约束条件
   - 实践：Our Method 提供工具清单和最佳实践

4. **输出结构化（Output Structuring）**
   - 理论：明确的输出格式提高质量和一致性
   - 实践：6字段详细输出 vs 3字段基础输出

5. **思维链引导（Chain-of-Thought Elicitation）**
   - 理论：引导逐步推理提高复杂任务表现
   - 实践：要求列举"key_signals"和"detailed reasoning"

---

## 实验控制变量

为确保实验的内部效度，以下变量在三种方法间保持严格一致：

### 控制变量（相同）
- ✓ 输入数据格式和内容
- ✓ LLM模型（GPT-3.5-turbo）
- ✓ 温度参数（0.7）
- ✓ 最大token数（1000）
- ✓ 数据集（88个交易日）
- ✓ 评估指标
- ✓ 随机种子

### 自变量（不同）
- ✗ 系统提示词（system prompt）设计

### 因变量（测量）
- 总收益率
- 夏普比率
- 准确率
- 胜率
- 交易次数
- 平均信心度

---

## 使用建议

### 论文中引用方式

**方式一：主文中简述 + 附录完整文本**

主文：
> 我们设计了三种不同复杂度的提示词策略：Baseline 1采用最简化的通用提示（30词），Baseline 3引入简单的角色定义（50词），Our Method使用详细的角色构建、工具清单和专业指导（156词）。完整提示词文本见附录A。

附录A：
> [本文档的"完整提示词文本"部分]

**方式二：对比表格**

在论文中使用"提示词设计维度对比"表格，展示关键差异。

**方式三：逐层展示**

分别展示三个提示词的完整文本，配以简短的设计说明。

---

## 可复现性声明

本研究的完整实验代码、数据集和提示词均已开源：

- **代码仓库**: https://github.com/LXW150324/LLM
- **分支**: claude/debug-code-setup-011CUKpEY2uq4GgHFidDqAsT
- **提示词文件**: `run_real_llm_experiment.py` (第99-158行)
- **数据集**: `data/AAPL_simulated_basic.csv`
- **完整报告**: `FINAL_EXPERIMENT_REPORT.md`

研究者可以使用提供的代码和数据集完全复现实验结果。

---

## 伦理与局限性说明

### 数据说明
本研究使用模拟数据（基于统计模型生成），而非真实市场数据。虽然数据遵循真实市场的统计规律，但结果不应用于实际交易决策。

### 提示词设计
所有提示词均为研究目的设计，旨在对比不同复杂度对LLM性能的影响，不代表最优的实际应用方案。

### 模型选择
实验使用GPT-3.5-turbo模型。不同模型（如GPT-4、Claude等）可能产生不同结果。

---

**文档版本**: 1.0
**最后更新**: 2025-10-30
**对应实验**: 多Agent股票交易预测系统 - 提示词策略对比实验
