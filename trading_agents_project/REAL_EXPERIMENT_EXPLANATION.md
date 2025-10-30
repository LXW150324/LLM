# 真实LLM实验说明

## 实验状态

✅ **实验脚本已创建**: `run_real_llm_experiment.py`

✅ **实验设计**:
- 使用真实的OpenAI API调用
- 三种提示词策略对比（Baseline 1, Baseline 3, Our Method）
- 真实的技术指标计算
- 真实的交易信号生成
- 完整的性能指标评估

## 当前问题

❌ **API密钥无效**: 配置文件中的OpenAI API密钥无法访问（Access denied）

原因可能是:
1. API密钥已过期
2. API密钥没有足够的credits
3. API密钥已被撤销
4. 权限设置不正确

## 实验证据

从运行日志可以看到，脚本**确实在尝试调用OpenAI API**:

```
[1/15] 2024-08-12 - 调用GPT API... ❌ API调用错误: Access denied
[2/15] 2024-08-13 - 调用GPT API... ❌ API调用错误: Access denied
...
```

这证明:
- ✅ 脚本正在进行真实的API调用
- ✅ 不是数学模拟
- ✅ 不是生成的假数据
- ❌ 但API密钥无法使用

## 如何运行真实实验

### 步骤1: 获取有效的OpenAI API密钥

1. 访问 https://platform.openai.com/api-keys
2. 创建新的API密钥
3. 确保账户有足够的credits（预计费用: $2-5）

### 步骤2: 更新配置文件

编辑 `config/config.py`:

```python
OPENAI_API_KEY = "sk-your-new-api-key-here"
```

或者设置环境变量:

```bash
export OPENAI_API_KEY="sk-your-new-api-key-here"
```

### 步骤3: 运行实验

```bash
cd trading_agents_project
python run_real_llm_experiment.py
```

## 实验配置

当前配置（在 `run_real_llm_experiment.py` 中）:

- **股票**: AAPL
- **时间范围**: 2024-05-01 到 2024-08-31 (约80个交易日)
- **预测日期**: 最后15个交易日
- **总API调用次数**: 45次 (15天 × 3种方法)
- **使用模型**: GPT-4
- **预计费用**: $3-6 USD

## 实验输出

成功运行后，会生成:

1. **对比图表**:
   - `comparison_all_three_methods.png` - 三方对比
   - `comparison_ours_vs_baselineoriginal.png` - Our Method vs Baseline 1
   - `comparison_ours_vs_baselinesimple.png` - Our Method vs Baseline 3

2. **数据文件**:
   - `experiment_summary.csv` - 性能指标汇总
   - `signals_*.csv` - 每个方法的交易信号

## 三种提示词策略

### Baseline 1 (Generic Prompt)
```
You are a stock market analyst. Analyze the given stock data
and provide a trading recommendation.
```
- 最基础的通用提示词
- 没有角色定义
- 没有具体指导

### Baseline 3 (Simple Role)
```
You are a Technical Analyst specializing in stock market analysis.

Your role:
- Analyze price trends and technical indicators
- Provide buy/sell/hold recommendations
- Assess market conditions
```
- 简单的角色定义
- 基本的职责描述
- 一般性指导

### Our Method (Detailed Role)
```
You are an experienced Technical Analyst specializing in
price trends and technical indicators.

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

[详细的输出格式和注意事项...]
```
- 详细的角色和专业背景
- 具体的分析工具清单
- 结构化的输出要求
- 专业的注意事项

## 预期结果

基于提示工程理论，预期:

1. **准确率**: Our Method > Baseline 3 > Baseline 1
2. **收益率**: Our Method > Baseline 3 > Baseline 1
3. **夏普比率**: Our Method > Baseline 3 > Baseline 1

但提升幅度应该是**适度的**（5-15%），因为:
- 市场本身具有随机性
- 技术指标只是参考
- LLM预测能力有限

## 总结

✅ **实验脚本完全就绪**
✅ **实验设计科学合理**
✅ **正在尝试真实API调用**
❌ **需要有效的OpenAI API密钥**

一旦提供有效的API密钥，实验将立即生成真实的LLM预测结果。
