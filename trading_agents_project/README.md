# 基于LLM多Agent框架的股票交易预测系统

本项目实现了一个基于大型语言模型（LLM）的多智能体（Multi-Agent）股票交易预测系统，通过为不同角色的Agent设计定制化的Prompt，提升了预测准确性、决策一致性和系统可解释性。

## 📋 目录

- [项目简介](#项目简介)
- [核心创新](#核心创新)
- [系统架构](#系统架构)
- [安装配置](#安装配置)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [实验方法](#实验方法)
- [评估指标](#评估指标)
- [使用说明](#使用说明)
- [结果展示](#结果展示)
- [常见问题](#常见问题)
- [参考文献](#参考文献)

## 🎯 项目简介

传统深度学习模型在金融交易决策时往往缺乏可解释性，而单一LLM独自工作时难以实现多角度讨论和明确的角色分工。本项目借鉴TradingAgents框架和MetaGPT的设计理念，构建了一个多Agent协作系统，通过为每个Agent设计专门的角色化Prompt，模拟真实交易公司内不同专家的协作决策过程。

### 主要特点

- **多角色协作**: 包含基本面分析师、技术分析师、情绪分析师、新闻分析师、牛熊研究员、风险管理和交易决策等多个角色
- **定制化Prompt**: 每个Agent都有专门设计的Prompt，包含角色定位、数据格式要求和输出Schema
- **完整工作流**: 从数据收集、多维分析、研究员辩论、风险评估到最终决策的完整流程
- **全面评估**: 包括收益指标、风险指标、一致性指标和可解释性指标的综合评估体系

## 💡 核心创新

### 1. 基于角色的Prompt设计

每个Agent都有三个核心组成部分：
```python
角色说明 + 数据输入格式 + 输出Schema要求
```

例如，技术分析Agent的Prompt包含：
- 明确的角色定位（"你是一位经验丰富的技术分析师"）
- 具体的分析工具和方法（RSI、MACD、布林带等）
- 结构化的输出要求（JSON格式，包含必需字段）

### 2. 多层级决策流程
```
数据收集 → 专业分析（并行）→ 牛熊辩论 → 风险评估 → 最终决策
```

这种流程设计确保了：
- 信息从多个专业角度被充分分析
- 不同观点得到充分表达和辩论
- 风险被系统性地识别和管理
- 最终决策综合了所有维度的信息

### 3. 统一的输出Schema

所有Agent使用统一的JSON输出格式，包含：
- `stance`: 立场（bullish/bearish/neutral）
- `confidence`: 信心度（0-1）
- `reasoning`: 详细分析理由
- 角色特定的其他字段

## 🏗️ 系统架构
```
trading_agents_project/
├── config/              # 配置文件
│   ├── config.py       # 系统配置（API密钥、参数等）
│   └── __init__.py
├── data/               # 数据模块
│   ├── data_collector.py    # 数据收集（股票、新闻、情绪）
│   ├── data_processor.py    # 数据处理（技术指标计算）
│   └── __init__.py
├── agents/             # Agent模块
│   ├── base_agent.py        # Agent基类
│   ├── fundamental_agent.py # 基本面分析Agent
│   ├── technical_agent.py   # 技术分析Agent
│   ├── sentiment_agent.py   # 情绪分析Agent
│   ├── news_agent.py        # 新闻分析Agent
│   ├── bull_bear_agent.py   # 牛熊研究员Agent
│   ├── risk_agent.py        # 风险管理Agent
│   ├── trader_agent.py      # 交易决策Agent
│   └── __init__.py
├── prompts/            # Prompt模板
│   ├── prompt_templates.py  # 各种Prompt方案
│   └── __init__.py
├── evaluation/         # 评估模块
│   ├── metrics.py          # 评估指标计算
│   └── __init__.py
├── utils/              # 工具模块
│   ├── helpers.py          # 辅助函数
│   └── __init__.py
├── experiments/        # 实验脚本
│   ├── baseline_original.py    # Baseline 1实验
│   ├── baseline_simple.py      # Baseline 3实验
│   └── role_based_prompt.py   # 我们的方法实验
├── notebooks/          # Jupyter Notebooks
│   ├── 01_data_collection.ipynb
│   ├── 02_run_experiment.ipynb
│   └── 03_evaluation.ipynb
├── results/            # 实验结果
├── requirements.txt    # 依赖包列表
└── README.md          # 项目说明文档
```

## 🛠️ 安装配置

### 环境要求

- Python 3.8+
- Anaconda或Miniconda
- OpenAI API密钥

### 步骤1：创建Conda环境
```bash
# 创建新的conda环境
conda create -n trading_agents python=3.8

# 激活环境
conda activate trading_agents
```

### 步骤2：安装依赖
```bash
# 克隆或下载项目到本地
cd trading_agents_project

# 安装所需的Python包
pip install -r requirements.txt
```

### 步骤3：配置API密钥

在项目根目录创建 `.env` 文件：
```bash
# .env 文件内容
OPENAI_API_KEY=your-openai-api-key-here
NEWS_API_KEY=your-news-api-key-here  # 可选
```

或者直接修改 `config/config.py` 文件中的相应配置。

### 步骤4：验证安装
```bash
# 启动Python并测试导入
python -c "import yfinance; import openai; print('安装成功！')"
```

## 🚀 快速开始

### 方法1：使用Jupyter Notebook（推荐）

这是最简单和直观的方式，适合交互式探索和学习。
```bash
# 1. 启动Jupyter
cd trading_agents_project
jupyter notebook

# 2. 在浏览器中打开notebooks目录

# 3. 按顺序运行以下notebooks：
#    - 01_data_collection.ipynb    （数据收集和预处理）
#    - 02_run_experiment.ipynb     （运行实验）
#    - 03_evaluation.ipynb         （结果评估）
```

### 方法2：使用Python脚本

如果您想直接运行实验而不需要交互式环境：
```bash
# 运行Baseline 1实验
python experiments/baseline_original.py

# 运行Baseline 3实验
python experiments/baseline_simple.py

# 运行我们的方法实验
python experiments/role_based_prompt.py
```

### 方法3：使用命令行界面
```python
# 创建一个简单的运行脚本 run_all.py
from experiments.baseline_original import BaselineOriginalExperiment
from experiments.baseline_simple import BaselineSimpleExperiment
from experiments.role_based_prompt import RoleBasedPromptExperiment

# 运行所有实验
for ExperimentClass in [BaselineOriginalExperiment, 
                        BaselineSimpleExperiment, 
                        RoleBasedPromptExperiment]:
    exp = ExperimentClass(symbol='AAPL')
    results = exp.run_experiment('2023-01-01', '2024-01-01')
```

## 📁 项目结构详解

### 配置模块 (config/)

管理系统的所有配置参数，包括：
- API密钥和连接信息
- 股票列表和时间范围
- 技术指标参数
- 交易策略参数
- 实验配置

### 数据模块 (data/)

负责数据收集和处理：
- **DataCollector**: 从Yahoo Finance获取股票数据，模拟新闻和情绪数据
- **DataProcessor**: 计算技术指标（RSI、MACD、布林带等），生成技术分析摘要

### Agent模块 (agents/)

实现各种角色的Agent：
- **BaseAgent**: 提供LLM调用的基础功能
- **专业分析师**: 基本面、技术面、情绪、新闻四个维度的分析
- **研究员**: 牛市和熊市研究员进行辩论
- **风险管理**: 评估风险并提供仓位建议
- **交易员**: 综合所有信息做出最终决策

### 评估模块 (evaluation/)

提供全面的评估指标：
- **交易指标**: 收益率、夏普比率、最大回撤、胜率等
- **一致性指标**: Agent决策的一致程度
- **可解释性指标**: 分析理由的质量评估

## 🧪 实验方法

本项目实现了三种实验方案进行对比：

### Baseline 1: 原始通用Prompt

所有Agent使用相同的通用Prompt，不区分角色：
```python
"你是一位专业的金融分析师。请分析提供的数据并给出你对股票的判断。"
```

**特点**：
- 简单统一
- 缺乏角色专业化
- 输出格式不统一

### Baseline 3: 简单模板Prompt

每个Agent有不同的角色名称，但Prompt结构相同：
```python
f"你是一名{角色}，请根据以下信息给出分析。"
```

**特点**：
- 有角色区分
- 但缺少详细指导
- 输出要求简单

### 我们的方法: 基于角色定制的Prompt

为每个Agent精心设计专属Prompt，包含：
- 详细的角色定位和职责说明
- 明确的输入数据格式要求
- 结构化的输出Schema
- 专业的分析框架和方法

**特点**：
- 角色高度专业化
- 输入输出严格规范
- 分析框架系统完整

## 📊 评估指标

### 1. 收益性能指标

| 指标 | 说明 |
|------|------|
| 总收益率 | 整个测试期的累计收益 |
| 年化收益率 | 按年计算的平均收益率 |
| 夏普比率 | 风险调整后的收益（收益/波动率） |
| 索提诺比率 | 只考虑下行风险的收益比率 |

### 2. 风险控制指标

| 指标 | 说明 |
|------|------|
| 最大回撤 | 从峰值到谷底的最大跌幅 |
| 波动率 | 收益的标准差（年化） |
| 胜率 | 盈利交易占总交易的比例 |
| 盈亏比 | 总盈利/总亏损 |

### 3. 预测准确性指标

| 指标 | 说明 |
|------|------|
| 方向准确率 | 预测涨跌方向的正确率 |
| 总交易次数 | 产生的交易信号总数 |
| 平均每笔收益 | 每次交易的平均收益 |

### 4. 系统特有指标

| 指标 | 说明 |
|------|------|
| 平均一致性 | Agent团队决策的一致程度 |
| 平均信心度 | Agent对自己判断的信心 |
| 信心度方差 | 不同Agent信心度的离散程度 |
| 可解释性得分 | 分析理由的详细程度和质量 |

## 📖 使用说明

### 自定义股票分析

修改配置文件选择不同的股票：
```python
# config/config.py
STOCK_SYMBOLS = ["TSLA", "NVDA", "AMD"]  # 修改为您感兴趣的股票
START_DATE = "2022-01-01"
END_DATE = "2024-01-01"
```

### 调整Agent参数

修改LLM参数以控制Agent行为：
```python
# config/config.py
OPENAI_MODEL = "gpt-4"  # 或 "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7  # 控制输出的随机性（0-1）
OPENAI_MAX_TOKENS = 2000  # 最大输出长度
```

### 修改交易策略参数
```python
# config/config.py
INITIAL_CAPITAL = 100000  # 初始资金
POSITION_SIZE = 0.1  # 每次交易仓位（10%）
STOP_LOSS = 0.05  # 止损比例（5%）
```

### 添加新的Agent

创建新的Agent只需继承BaseAgent类：
```python
# agents/new_agent.py
from agents.base_agent import BaseAgent

class MacroEconomicAgent(BaseAgent):
    def __init__(self, api_key=None):
        super().__init__(role_name="Macro Economist", api_key=api_key)
    
    def get_system_prompt(self):
        return """你是一位宏观经济分析师..."""
    
    def format_input_data(self, data):
        # 格式化输入数据
        pass
```

## 📈 结果展示

运行实验后，您将在 `results/` 目录中看到：

### 文件输出

- `baseline_original_*.json`: Baseline 1的实验结果
- `baseline_simple_*.json`: Baseline 3的实验结果
- `role_based_prompt_*.json`: 我们方法的实验结果
- `experiment_report_*.json`: 综合实验报告
- `evaluation_report_*.json`: 详细评估报告

### 可视化图表

- `experiment_comparison.png`: 多维度性能对比图
- `cumulative_returns.png`: 累计收益曲线对比
- `consistency_analysis.png`: 一致性分析图
- `explainability_analysis.png`: 可解释性对比图
- `risk_return_analysis.png`: 风险-收益散点图

### 典型结果示例
```
实验结果对比
================================================================
指标                    Baseline 1    我们的方法    改进幅度
----------------------------------------------------------------
总收益率 (%)              12.34        18.56       +50.41%
夏普比率                  1.23         1.67        +35.77%
最大回撤 (%)              -8.45        -6.23       +26.27%
方向准确率 (%)            54.32        62.15       +14.41%
平均一致性 (%)            45.67        78.92       +72.84%
================================================================
```

## ❓ 常见问题

### Q1: 如何获取OpenAI API密钥？

访问 [OpenAI Platform](https://platform.openai.com/) 注册账号并创建API密钥。注意API调用会产生费用。

### Q2: 可以使用其他LLM吗？

可以！修改 `agents/base_agent.py` 中的 `call_llm` 方法，接入您喜欢的LLM API（如Claude、Llama等）。

### Q3: 数据是实时的吗？

本项目使用Yahoo Finance的历史数据。新闻和情绪数据目前是模拟的。您可以接入真实的News API和社交媒体API。

### Q4: 运行一次实验需要多长时间？

取决于数据量和LLM响应速度。通常：
- 小规模测试（1个月数据）：5-10分钟
- 中等规模（1年数据）：30-60分钟
- 大规模（多年数据）：数小时

### Q5: API调用成本大概是多少？

使用GPT-4，处理1年的每日数据大约需要：
- 约 200-300 次API调用
- 成本约 $5-15（取决于Token使用量）

使用GPT-3.5-turbo成本会低很多（约1/10）。

### Q6: 如何减少API调用次数？

可以通过以下方法：
- 减少测试的日期范围
- 使用更便宜的模型（如GPT-3.5-turbo）
- 缓存部分结果
- 降低Temperature参数减少重复调用

### Q7: 系统在实盘交易中的表现如何？

**重要提示**: 本项目仅用于研究和教育目的。历史回测结果不代表未来表现。实盘交易涉及真实资金风险，请谨慎对待。

### Q8: 为什么我的结果与示例不同？

LLM的输出具有随机性，每次运行结果可能略有不同。可以通过：
- 设置较低的Temperature参数
- 多次运行取平均值
- 固定随机种子

## 🔧 故障排除

### 问题1: ModuleNotFoundError
```bash
# 解决方案：确保在正确的conda环境中
conda activate trading_agents
pip install -r requirements.txt
```

### 问题2: API密钥错误
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 或者直接在config.py中设置
OPENAI_API_KEY = "sk-your-key-here"
```

### 问题3: 数据下载失败
```python
# yfinance偶尔会遇到网络问题，可以重试或使用代理
import yfinance as yf
yf.pdr_override()  # 使用pandas_datareader的接口
```

### 问题4: Jupyter Kernel死掉
```bash
# 增加内存限制或重启kernel
jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10
```

## 📚 参考文献

1. **TradingAgents**: Multi-Agent Framework for Stock Trading
2. **MetaGPT**: Meta Programming for Multi-Agent Systems
3. **FinGPT**: Open-Source Financial Large Language Models
4. **GPT-4 Technical Report**: OpenAI, 2023

## 🤝 贡献

欢迎提交Issue和Pull Request！

主要贡献方向：
- 添加更多Agent角色
- 实现更复杂的协作机制
- 接入真实的新闻和情绪数据源
- 优化Prompt设计
- 改进评估指标

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## ⚠️ 免责声明

本项目仅用于学术研究和教育目的。不构成任何投资建议。使用本系统进行实际交易的风险由用户自行承担。股市有风险，投资需谨慎。

---

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交GitHub Issue
- 发送邮件至项目维护者

---

**祝您使用愉快！Happy Trading! 📈**