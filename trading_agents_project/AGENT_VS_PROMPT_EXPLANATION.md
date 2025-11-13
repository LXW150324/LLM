# Agent与Prompt的关系详解

## 核心概念

### Agent（智能体）
一个具有特定角色和职责的AI助手，由**代码框架 + 提示词 + LLM**组成。

### Prompt（提示词）
告诉LLM如何扮演Agent角色的**指令文本**。

### 关系
**Prompt是Agent的核心组成部分**，是Agent的"灵魂配置"。

---

## 具体示例：技术分析师Agent

### 1. Agent的代码结构

```python
# agents/technical_agent.py

class TechnicalAnalysisAgent:
    """技术分析师Agent"""

    def __init__(self, api_key):
        self.role_name = "Technical Analyst"  # Agent角色名称
        self.client = OpenAI(api_key=api_key)  # LLM客户端
        self.model = "gpt-4"

    def get_system_prompt(self):
        """
        这里返回的就是Prompt（提示词）！
        它定义了这个Agent的角色、职责、工具、输出格式
        """
        return """你是一位经验丰富的技术分析师，专注于价格走势和技术指标分析。

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
请以JSON格式输出你的分析结果...
"""

    def format_input_data(self, data):
        """
        这里构建User Prompt（用户提示词）
        提供具体的数据和问题
        """
        return f"""请分析以下 AAPL 股票的技术面数据：

价格信息:
- 当前价: ${data['close']:.2f}
- 开盘价: ${data['open']:.2f}
...

请基于以上技术指标，评估 AAPL 的技术面。
"""

    def analyze(self, data):
        """
        Agent的核心工作流程：
        1. 获取System Prompt（定义角色）
        2. 构建User Prompt（提供数据）
        3. 调用LLM
        4. 解析结果
        5. 返回分析报告
        """
        # 步骤1：获取Agent的角色定义（System Prompt）
        system_prompt = self.get_system_prompt()

        # 步骤2：准备具体问题（User Prompt）
        user_prompt = self.format_input_data(data)

        # 步骤3：调用LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},  # ← Prompt在这里使用！
                {"role": "user", "content": user_prompt}       # ← Prompt在这里使用！
            ]
        )

        # 步骤4：解析LLM的响应
        analysis_result = self.parse_response(response)

        # 步骤5：返回分析报告
        return analysis_result

    def parse_response(self, response):
        """解析LLM返回的JSON"""
        content = response.choices[0].message.content
        return json.loads(content)
```

---

## Agent的组成部分

一个完整的Agent包含：

### 1. 代码框架（Class定义）
```python
class TechnicalAnalysisAgent(BaseAgent):
    def __init__(self, api_key):
        # 初始化

    def analyze(self, data):
        # 分析逻辑

    def parse_response(self, response):
        # 解析结果
```

**作用**: 提供Agent的运行逻辑、数据处理、错误处理等

### 2. System Prompt（系统提示词）
```python
def get_system_prompt(self):
    return """你是一位经验丰富的技术分析师...

你的职责：
1. 分析价格趋势
2. 解读技术指标
...

输出要求：
JSON格式...
"""
```

**作用**: 告诉LLM它是谁、要做什么、怎么做

### 3. User Prompt（用户提示词）
```python
def format_input_data(self, data):
    return f"""请分析以下数据：

价格: ${data['close']}
RSI: {data['rsi']}
...
"""
```

**作用**: 提供具体的数据和问题

### 4. LLM调用逻辑
```python
response = self.client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
)
```

**作用**: 与LLM API通信

### 5. 响应解析逻辑
```python
def parse_response(self, response):
    content = response.choices[0].message.content
    return json.loads(content)
```

**作用**: 将LLM的文本输出转换为结构化数据

---

## 关键理解

### Prompt是Agent的"配置文件"

想象一下：

```
Agent = 一台电脑
Prompt = 这台电脑安装的操作系统和软件

同样的硬件（LLM模型），安装不同的软件（Prompt），
就变成了不同功能的电脑（Agent）。
```

### 同一个LLM，不同的Prompt = 不同的Agent

```python
# 使用相同的GPT-4模型

# Agent 1: 技术分析师
technical_agent = TechnicalAnalysisAgent(api_key)
# 它的Prompt是："你是技术分析师，分析价格和指标..."

# Agent 2: 基本面分析师
fundamental_agent = FundamentalAnalysisAgent(api_key)
# 它的Prompt是："你是基本面分析师，分析财务和估值..."

# Agent 3: 情绪分析师
sentiment_agent = SentimentAnalysisAgent(api_key)
# 它的Prompt是："你是情绪分析师，分析社交媒体..."
```

**同一个LLM（GPT-4），但因为Prompt不同，表现出不同的"专业角色"！**

---

## 实际运行示例

### 输入数据
```python
data = {
    'symbol': 'AAPL',
    'close': 173.94,
    'rsi': 47.09,
    'macd': 0.0112,
    ...
}
```

### Agent处理流程

```
1. 【准备System Prompt】
   system_prompt = "你是一位经验丰富的技术分析师..."

2. 【准备User Prompt】
   user_prompt = "请分析以下AAPL数据：价格$173.94, RSI 47.09..."

3. 【发送给LLM】
   GPT-4收到两个Prompt：
   - System: "你是技术分析师..." （告诉它角色）
   - User: "分析AAPL数据..." （告诉它任务）

4. 【LLM思考】
   "我是技术分析师，我要分析这些技术指标...
    RSI 47在中性区域，MACD略显金叉..."

5. 【LLM输出】
   {
       "stance": "neutral",
       "confidence": 0.6,
       "trend_direction": "sideways",
       ...
   }

6. 【Agent解析】
   将JSON转换为Python字典，返回结果
```

---

## 多Agent系统示例

在你的原始项目中，有5个不同的Agents：

```python
# 1. 技术分析师Agent
technical_agent = TechnicalAnalysisAgent(api_key)
technical_report = technical_agent.analyze(technical_data)

# 2. 基本面分析师Agent
fundamental_agent = FundamentalAnalysisAgent(api_key)
fundamental_report = fundamental_agent.analyze(financial_data)

# 3. 情绪分析师Agent
sentiment_agent = SentimentAnalysisAgent(api_key)
sentiment_report = sentiment_agent.analyze(sentiment_data)

# 4. 新闻分析师Agent
news_agent = NewsAnalysisAgent(api_key)
news_report = news_agent.analyze(news_data)

# 5. 交易决策Agent（综合前面4个报告）
trader_agent = TraderAgent(api_key)
final_decision = trader_agent.make_decision({
    'technical': technical_report,
    'fundamental': fundamental_report,
    'sentiment': sentiment_report,
    'news': news_report
})
```

**每个Agent都有自己的Prompt，定义了自己的角色和职责！**

---

## 对比：Agent vs Prompt

| 维度 | Agent | Prompt |
|------|-------|--------|
| **是什么** | 整个系统/框架 | 文本指令 |
| **包含** | 代码+Prompt+逻辑 | 纯文本 |
| **作用** | 完成特定任务 | 告诉LLM如何思考 |
| **类比** | 一个专业顾问 | 顾问的职位说明书 |
| **可见性** | 抽象概念 | 具体文本 |
| **修改** | 修改代码 | 修改文本 |

---

## 为什么容易混淆？

### 在简单场景下：

```python
# 简单脚本（没有Agent类）
prompt = "你是技术分析师，分析这些数据：..."

response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

在这种情况下，**只有Prompt，没有Agent类**。

### 在复杂系统中：

```python
# 有Agent类
class TechnicalAnalysisAgent:
    def get_system_prompt(self):
        return "你是技术分析师..."

    def analyze(self, data):
        prompt = self.get_system_prompt()
        # ... 调用LLM ...
```

在这种情况下，**Prompt是Agent的一部分**。

---

## 核心总结

### 1. Agent是整体概念
```
Agent = {
    代码框架（20%） +
    System Prompt（40%） +  ← 最重要！定义角色
    User Prompt（20%） +
    LLM调用（10%） +
    响应解析（10%）
}
```

### 2. Prompt是Agent的核心
**System Prompt定义了Agent是谁、做什么、怎么做**，是Agent的"灵魂"。

### 3. 修改Prompt = 修改Agent的行为
```python
# 同样的代码框架，不同的Prompt

# Prompt 1: "你是保守的分析师，只推荐低风险投资"
# → 得到保守的Agent

# Prompt 2: "你是激进的分析师，寻找高回报机会"
# → 得到激进的Agent
```

### 4. 在论文中
- **展示Agent设计** = 展示系统架构、工作流程
- **展示Prompt** = 展示具体的角色定义文本

**两者是包含关系**：Agent包含Prompt，Prompt是Agent的核心配置。

---

## 你的项目中的情况

### 原始设计（5个Agents）

```
TechnicalAnalysisAgent
├── 代码框架（technical_agent.py）
├── System Prompt（技术分析师角色定义）← 这就是提示词！
├── User Prompt格式化逻辑
└── LLM调用和解析逻辑

FundamentalAnalysisAgent
├── 代码框架（fundamental_agent.py）
├── System Prompt（基本面分析师角色定义）← 这就是提示词！
├── User Prompt格式化逻辑
└── LLM调用和解析逻辑

... (其他3个Agents类似)
```

### 实验简化版本（1个Agent，3种Prompt）

```
同一个Agent代码框架，使用3种不同的Prompt：

Prompt版本1: Baseline 1（简单通用）
Prompt版本2: Baseline 3（简单角色）
Prompt版本3: Our Method（详细角色）

→ 测试不同Prompt对Agent性能的影响
```

---

## 形象比喻

```
Agent = 一个演员
Prompt = 剧本和角色说明

同一个演员（GPT-4），拿到不同的剧本（Prompt）：
- 剧本1："你是技术分析师" → 演出技术分析师
- 剧本2："你是基本面分析师" → 演出基本面分析师
- 剧本3："你是交易员" → 演出交易员

演员的演技（LLM能力）是固定的，
但剧本（Prompt）决定了他演什么角色、怎么演！
```

---

**现在清楚了吗？**

简单总结：
- **Agent = 完整的系统**（代码+提示词+逻辑）
- **Prompt = Agent的配置文件**，告诉LLM如何扮演这个Agent
- **关系 = Prompt是Agent的核心组成部分**

论文中：
- 展示"Agent设计" = 展示系统架构图、工作流程
- 展示"Prompt" = 展示具体的角色定义文本（最重要！）

你想展示哪个层面，或者两者都展示？
