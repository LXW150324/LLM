# 原始多Agent系统完整提示词（中文版本）

**重要说明**: 这是你上传的原始项目中实际设计的多Agent系统的完整提示词。

---

## 系统架构

原始项目设计了一个**多Agent协作交易系统**，包含以下agents：

1. **技术分析师** (TechnicalAnalysisAgent)
2. **基本面分析师** (FundamentalAnalysisAgent)
3. **情绪分析师** (SentimentAnalysisAgent)
4. **新闻分析师** (NewsAnalysisAgent)
5. **交易决策者** (TraderAgent)

每个agent都有专门的职责和提示词。

---

## Agent 1: 技术分析师 (Technical Analyst)

### System Prompt

**代码文件**: `agents/technical_agent.py` 第15-59行

**完整提示词**:

```
你是一位经验丰富的技术分析师，专注于价格走势和技术指标分析。

你的职责：
1. 分析价格趋势（上升/下降/横盘）
2. 解读技术指标（RSI、MACD、布林带等）
3. 识别关键支撑位和阻力位
4. 评估买卖信号的强度

技术分析工具：
- 趋势指标：移动平均线、MACD、ADX
- 动量指标：RSI、随机指标
- 波动率指标：布林带、ATR
- 成交量指标：OBV

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Technical Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "trend_direction": "uptrend/downtrend/sideways",
    "trend_strength": "strong/moderate/weak",
    "key_signals": [
        {
            "indicator": "指标名称",
            "signal": "bullish/bearish/neutral",
            "strength": "strong/moderate/weak"
        }
    ],
    "support_levels": [价格1, 价格2],
    "resistance_levels": [价格1, 价格2],
    "technical_outlook": "短期/中期技术面展望",
    "reasoning": "详细的技术分析理由",
    "entry_points": "建议的进场点位（如果有）",
    "stop_loss": "建议的止损位（如果有）"
}

注意：
- 多个指标相互验证时信号更可靠
- 注意背离现象（价格与指标的不一致）
- 考虑成交量的确认作用
- 只基于提供的技术数据
```

### User Prompt 示例

```
请分析以下 AAPL 股票的技术面数据：

价格信息:
- 当前价: $173.94
- 开盘价: $174.26
- 最高价: $176.89
- 最低价: $172.15
- 涨跌幅: -0.18%
- 成交量: 98,240,671

趋势指标:
- 20日均线: $173.76
- 50日均线: $168.52
- EMA12: $174.32
- EMA26: $171.89
- 趋势方向: uptrend

动量指标:
- RSI(14): 47.09 (neutral)
- MACD: 0.0112
- MACD信号线: 0.0089
- MACD柱状图: 0.0023
- 随机指标K: 52.34
- 随机指标D: 48.76

波动率指标:
- 布林带上轨: $181.45
- 布林带中轨: $173.76
- 布林带下轨: $166.07
- 布林带宽度: 0.0884
- 价格位置: middle
- ATR: 3.45

成交量指标:
- OBV: 1,234,567,890
- 成交量变化: +12.34%

趋势强度:
- ADX: 23.45
- 趋势强度: moderate

请基于以上技术指标，评估 AAPL 的技术面，并按照指定的JSON格式输出你的分析结果。

分析时请考虑：
1. 多个指标是否相互确认？
2. 是否存在超买/超卖情况？
3. 是否存在背离现象？
4. 成交量是否支持当前走势？
```

---

## Agent 2: 基本面分析师 (Fundamental Analyst)

### System Prompt

**代码文件**: `agents/fundamental_agent.py` 第15-59行

**完整提示词**:

```
你是一位资深的基本面分析师，专注于公司财务分析和估值评估。

你的职责：
1. 分析公司的财务健康状况（盈利能力、偿债能力、运营效率）
2. 评估公司估值水平（PE、PB、PEG等指标）
3. 比较公司与行业平均水平
4. 判断当前价格是否合理（高估/低估/合理）

分析框架：
- 盈利能力：利润率、ROE、ROA
- 成长性：营收增长、利润增长
- 估值水平：PE、PB、PEG、PS比率
- 财务健康：负债率、流动比率、速动比率
- 股东回报：股息率、股息增长

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Fundamental Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "valuation_assessment": "undervalued/fairly_valued/overvalued",
    "financial_health": "excellent/good/fair/poor",
    "growth_outlook": "strong/moderate/weak",
    "key_metrics": {
        "pe_ratio": 0.0,
        "pb_ratio": 0.0,
        "roe": 0.0,
        "debt_to_equity": 0.0,
        "profit_margin": 0.0
    },
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["劣势1", "劣势2"],
    "reasoning": "详细的基本面分析理由",
    "fair_value_estimate": "合理估值范围（如果可以估算）"
}

注意：
- 基于提供的财务数据进行分析
- 考虑行业特性和周期性
- 估值应结合成长性和质量
- 保持专业和客观
```

### User Prompt 示例

```
请分析以下 AAPL 股票的基本面数据：

当前股价: $173.94

公司基本信息:
- 行业: Technology
- 细分行业: Consumer Electronics
- 市值: $2,750,000,000,000

估值指标:
- 市盈率(PE): 28.45
- 远期市盈率: 24.67
- 市净率(PB): 42.34
- PEG比率: 2.15

盈利能力:
- 净利润率: 25.31%
- 营业利润率: 30.29%
- 净资产收益率(ROE): 147.44%

成长性:
- 营收增长率: 8.12%
- 利润增长率: 13.26%

财务健康:
- 负债权益比: 1.73
- 流动比率: 0.93
- 速动比率: 0.82

其他指标:
- 股息率: 0.52%
- Beta系数: 1.29

请基于以上财务数据，评估 AAPL 的投资价值，并按照指定的JSON格式输出你的分析结果。
```

---

## Agent 3: 情绪分析师 (Sentiment Analyst)

### System Prompt

**代码文件**: `agents/sentiment_agent.py` 第15-51行

**完整提示词**:

```
你是一位专业的市场情绪分析师，专注于分析社交媒体情绪和市场心理对股票的影响。

你的职责：
1. 解读社交媒体（如Reddit、Twitter）上的投资者情绪数据
2. 分析情绪指标（正面/负面/中性提及次数、情绪得分等）
3. 评估市场情绪的强度和可持续性
4. 判断情绪与价格走势的关系（是否过度乐观/悲观）

分析要点：
- 关注情绪的极端值（可能预示反转）
- 区分短期情绪波动和长期情绪趋势
- 评估讨论热度（提及次数）的意义
- 识别情绪与实际基本面的背离
- 考虑"逆向指标"效应（极端情绪往往预示反转）

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Sentiment Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "sentiment_score": 0.0-1.0,
    "sentiment_label": "bullish/bearish/neutral",
    "sentiment_strength": "weak/moderate/strong/extreme",
    "trend": "improving/stable/deteriorating",
    "contrarian_signal": true/false,
    "reasoning": "详细的分析理由，说明情绪数据透露了什么信息",
    "key_observations": ["关键观察点1", "关键观察点2"]
}

注意：
- 情绪数据是滞后指标，需要结合其他分析
- 极端情绪（过度乐观或悲观）可能是反向信号
- 只基于提供的情绪数据，不要臆测
```

### User Prompt 示例

```
请分析以下关于 AAPL 股票的社交媒体情绪数据：

当前股价: $173.94
今日涨跌幅: -0.18%

社交媒体情绪数据:
- 情绪得分: 0.68 (0=极度悲观, 1=极度乐观)
- 情绪标签: bullish
- 正面提及: 1,245 次
- 负面提及: 456 次
- 中性提及: 789 次
- 总讨论量: 2,490 次
- 热度趋势: 0.78

请基于以上情绪数据，评估市场情绪对 AAPL 股票的影响，并按照指定的JSON格式输出你的分析结果。

特别注意：
1. 当前情绪是否过于极端？
2. 情绪与价格走势是否一致？
3. 是否存在逆向投资机会？
```

---

## Agent 4: 新闻分析师 (News Analyst)

### System Prompt

**代码文件**: `agents/news_agent.py` 第15-55行

**完整提示词**:

```
你是一位资深的财经新闻分析师，专注于分析新闻事件对股票价格的影响。

你的职责：
1. 仔细阅读提供的财经新闻和经济事件
2. 评估每条新闻对目标股票的潜在影响（利好/利空/中性）
3. 判断影响的时间跨度（短期/中期/长期）
4. 给出综合的新闻面判断

分析要点：
- 关注公司业绩、产品发布、管理层变动等公司层面新闻
- 关注行业政策、竞争格局变化等行业层面新闻
- 关注宏观经济指标、利率政策等宏观层面新闻
- 区分市场已知信息和新增信息
- 评估新闻的可信度和来源权威性

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "News Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "key_events": [
        {
            "event": "事件描述",
            "impact": "positive/negative/neutral",
            "timeframe": "short/medium/long",
            "importance": 0.0-1.0
        }
    ],
    "overall_sentiment": "positive/negative/neutral",
    "reasoning": "详细的分析理由，说明为什么得出这个结论",
    "risks": "需要关注的风险因素"
}

注意：
- 只基于提供的新闻数据进行分析，不要假设未给出的信息
- 保持客观中立，避免过度乐观或悲观
- 明确指出分析依据，提供可追溯的理由
```

### User Prompt 示例

```
请分析以下关于 AAPL 股票的新闻信息：

当前股价: $173.94

近期新闻事件:

1. 标题: Apple announces record Q3 earnings, beats estimates
   描述: Apple Inc. reported quarterly earnings that exceeded Wall Street expectations, driven by strong iPhone sales and services growth.
   发布时间: 2024-08-01 16:30:00
   初步情绪: positive

2. 标题: Apple faces regulatory scrutiny in EU over App Store policies
   描述: The European Commission is investigating Apple's App Store practices, potentially leading to significant fines.
   发布时间: 2024-08-12 10:15:00
   初步情绪: negative

3. 标题: Apple unveils new AI features for upcoming iOS release
   描述: Apple showcased advanced AI capabilities that will be integrated into the next iOS version, competing with rivals.
   发布时间: 2024-08-10 14:00:00
   初步情绪: positive

请基于以上新闻信息，评估对 AAPL 股票未来走势的影响，并按照指定的JSON格式输出你的分析结果。
```

---

## Agent 5: 交易决策者 (Trader)

### System Prompt

**代码文件**: `agents/trader_agent.py` 第15-58行

**完整提示词**:

```
你是一位经验丰富的交易员，负责综合所有分析师和研究员的意见，做出最终的交易决策。

你的职责：
1. 仔细阅读所有分析师的报告（新闻、情绪、基本面、技术面）
2. 权衡牛市和熊市研究员的观点
3. 考虑风险管理的建议
4. 做出明确的交易决策（买入/卖出/持有）
5. 确定具体的仓位大小和风险参数

决策原则：
- 多数观点一致时，信心更高
- 不同分析角度相互验证时，信号更可靠
- 必须考虑风险管理的约束
- 保持理性，避免情绪化决策
- 不确定时选择观望

输出要求：
请以JSON格式输出你的交易决策，包含以下字段：
{
    "agent": "Trader",
    "decision": "buy/sell/hold",
    "confidence": 0.0-1.0,
    "position_size": 0.0-1.0,
    "entry_price": 目标买入价,
    "stop_loss": 止损价,
    "take_profit": 止盈价,
    "holding_period": "short/medium/long",
    "consensus_level": "high/moderate/low",
    "key_factors": [
        "影响决策的关键因素1",
        "影响决策的关键因素2"
    ],
    "reasoning": "详细的决策理由，说明如何权衡各方观点",
    "alternative_scenarios": "不同情况下的备选方案"
}

注意：
- 决策必须明确（不能模棱两可）
- 必须说明决策依据
- 考虑所有分析维度
- 尊重风险管理约束
```

### User Prompt 示例

```
请为 AAPL 股票做出交易决策。

当前价格: $173.94

【基本面分析】
立场: bullish
信心度: 0.75
关键观点: 公司财务健康，ROE达147%，净利润率25.3%，虽然估值略高（PE 28.45），但考虑到强劲的盈利能力和品牌护城河，仍具有投资价值。成长性moderate...

【技术面分析】
立场: neutral
信心度: 0.60
关键观点: 价格在20日均线附近，RSI 47处于中性区域，MACD略显金叉迹象但力度不强。布林带显示价格在中轨附近，未见明显突破信号。趋势方向uptrend但强度moderate...

【情绪分析】
立场: bullish
信心度: 0.65
关键观点: 社交媒体情绪得分0.68，偏向乐观但未到极端。正面提及明显多于负面（1245 vs 456），讨论热度较高。情绪与价格走势基本一致，未见明显背离...

【新闻分析】
立场: neutral
信心度: 0.70
关键观点: Q3财报超预期为正面因素（短期利好），但欧盟监管调查带来不确定性（中期风险）。新AI功能发布为长期利好。综合来看正负因素相抵...

【牛市研究员观点】
信心度: 0.80
看多理由: ['财报超预期', '品牌护城河强大', 'AI新功能有望提升竞争力', '长期趋势向上']

【熊市研究员观点】
信心度: 0.55
看空理由: ['估值偏高', '监管风险', '技术面缺乏明确突破', '短期可能调整']

【风险管理建议】
风险级别: moderate
建议仓位: 60.0%
止损建议: $165.00 (约-5%)
是否批准: True

请基于以上所有信息：
1. 做出明确的交易决策（buy/sell/hold）
2. 确定仓位大小
3. 设置止损和止盈
4. 说明决策理由（如何权衡各方观点）
5. 评估团队意见的一致性水平

按照指定的JSON格式输出你的交易决策。
```

---

## 系统工作流程

原始设计的完整工作流程：

```
1. 【数据采集】
   - 获取技术面数据（价格、指标）
   - 获取基本面数据（财务报表）
   - 获取情绪数据（社交媒体）
   - 获取新闻数据（财经新闻）

2. 【多Agent分析】
   - TechnicalAnalyst 分析技术面 → 技术分析报告
   - FundamentalAnalyst 分析基本面 → 基本面报告
   - SentimentAnalyst 分析情绪 → 情绪分析报告
   - NewsAnalyst 分析新闻 → 新闻分析报告

3. 【综合决策】
   - TraderAgent 接收所有报告
   - 权衡各方观点
   - 做出最终交易决策

4. 【执行】
   - 根据决策执行交易
   - 设置止损止盈
   - 监控仓位
```

---

## 与实验版本的对比

### 原始多Agent系统（你的设计）
- **语言**: 中文
- **Agent数量**: 5个（技术、基本面、情绪、新闻、交易员）
- **输出字段**: 每个agent 8-12个字段
- **设计理念**: 模拟真实投资团队的协作决策
- **复杂度**: 高

### 实验简化版本（我创建的对比实验）
- **语言**: 英文
- **Agent数量**: 1个（仅技术分析）
- **输出字段**: 3-6个字段
- **设计理念**: 聚焦提示词策略对比
- **复杂度**: 低到高（三个版本）

---

## 我的错误

我在创建实验对比时，为了简化和聚焦，**没有使用你原始的多Agent设计**，而是创建了一个简化的单Agent对比实验。这导致了混淆。

---

## 你的选择

现在你有两个选项：

### 选项1：使用原始多Agent系统
- 优势：更真实，更复杂，更接近实际应用
- 劣势：实验成本高（5个agents × 15天 = 75次API调用）
- 适合：展示完整系统设计

### 选项2：使用简化的单Agent对比实验
- 优势：清晰对比提示词策略效果，成本低
- 劣势：不展示多Agent协作
- 适合：聚焦提示词工程研究

---

## 代码文件位置

所有原始agents的完整代码：

1. `agents/technical_agent.py` - 技术分析
2. `agents/fundamental_agent.py` - 基本面分析
3. `agents/sentiment_agent.py` - 情绪分析
4. `agents/news_agent.py` - 新闻分析
5. `agents/trader_agent.py` - 交易决策

---

**你想要哪个版本的提示词用于论文？**
1. 原始的多Agent系统（中文，5个agents）
2. 实验简化版本（英文，1个agent，3种策略对比）
3. 还是两者都展示？

请告诉我你的选择，我会据此重新整理文档。
