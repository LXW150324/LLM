# Anaconda环境配置和运行指南

本文档详细说明如何在Anaconda中设置和运行此项目。

## 前提条件

1. 已安装Anaconda或Miniconda
2. 有可用的OpenAI API密钥（需要付费或有免费额度）
3. 稳定的网络连接（用于下载数据）

## 步骤1：创建Conda虚拟环境

打开Anaconda Prompt（Windows）或终端（Mac/Linux），执行以下命令：

```bash
# 创建新的conda环境，命名为trading_agents，使用Python 3.10
conda create -n trading_agents python=3.10 -y

# 激活环境
conda activate trading_agents
```

> **注意**：环境名称可以自定义，但建议使用`trading_agents`以保持一致性。

## 步骤2：进入项目目录

```bash
# 进入项目目录（根据你的实际路径修改）
cd /path/to/LLM/trading_agents_project

# 例如在Windows：
# cd C:\Users\YourName\LLM\trading_agents_project

# 例如在Mac/Linux：
# cd ~/LLM/trading_agents_project
```

## 步骤3：安装依赖包

```bash
# 安装所有必需的Python包
pip install -r requirements.txt
```

安装过程可能需要5-10分钟，取决于网络速度。

### 常见安装问题及解决方案

**问题1：安装ta-lib失败**
```bash
# 如果安装pandas-ta失败，可以单独安装
pip install pandas-ta --no-deps
pip install ta
```

**问题2：网络超时**
```bash
# 使用国内镜像源（中国用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**问题3：权限错误**
```bash
# 添加--user参数
pip install -r requirements.txt --user
```

## 步骤4：配置API密钥

### 方法A：使用环境变量（推荐）

创建`.env`文件：

```bash
# 在项目根目录创建.env文件
# Windows用户可以使用记事本创建
# Mac/Linux用户可以使用以下命令
touch .env
```

编辑`.env`文件，添加以下内容：

```
OPENAI_API_KEY=sk-你的OpenAI密钥
NEWS_API_KEY=你的News密钥（可选）
```

### 方法B：直接修改配置文件

编辑`config/config.py`文件，找到第28行，修改：

```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-你的实际密钥")
```

> **安全提示**：不要将包含真实API密钥的代码提交到Git仓库！

## 步骤5：验证安装

```bash
# 测试Python环境和包导入
python -c "import yfinance; import openai; import pandas; print('✅ 所有依赖安装成功！')"
```

如果看到"✅ 所有依赖安装成功！"，说明环境配置正确。

## 步骤6：运行项目

### 选项A：使用Jupyter Notebook（推荐新手）

```bash
# 启动Jupyter Notebook
jupyter notebook
```

浏览器会自动打开，然后：
1. 导航到`notebooks/`目录
2. 打开`Untitled.ipynb`或创建新的notebook
3. 按单元格逐步运行代码

### 选项B：运行实验脚本（推荐有经验用户）

```bash
# 运行简单模板实验（较快，成本较低）
python experiments/baseline_simple.py

# 运行原始方法实验
python experiments/baseline_original.py

# 运行基于角色的Prompt实验（我们的方法）
python experiments/role_based_prompt.py
```

### 选项C：交互式Python测试

```bash
# 启动Python交互式环境
python
```

然后输入以下代码：

```python
from config.config import config
from data.data_collector import DataCollector

# 测试数据收集
collector = DataCollector(['AAPL'])
data = collector.collect_all_data('AAPL', '2024-01-01', '2024-02-01')

print("成功收集数据！")
print(f"价格数据条数: {len(data['price_data'])}")
print(f"财务数据: {data['financial_data'].keys()}")
```

## 步骤7：查看结果

运行完成后，结果保存在`results/`目录：

```bash
# 查看结果目录
ls results/

# 或在Windows:
# dir results
```

结果文件包括：
- `*.json`：详细的实验结果数据
- `*.png`：可视化图表（如果生成）
- `*.csv`：表格数据

## 运行参数调整

### 减少API调用成本

编辑`config/config.py`：

```python
# 修改股票列表（减少股票数量）
STOCK_SYMBOLS = ["AAPL"]  # 只测试一个股票

# 缩短测试时间范围
START_DATE = "2024-01-01"
END_DATE = "2024-01-31"  # 只测试1个月

# 使用更便宜的模型
OPENAI_MODEL = "gpt-3.5-turbo"  # 而不是"gpt-4"
```

### 调整实验参数

```python
# 修改运行次数
NUM_RUNS = 1  # 只运行1次，默认是5次

# 修改温度参数
OPENAI_TEMPERATURE = 0.3  # 降低随机性
```

## 常见错误及解决方案

### 错误1：ModuleNotFoundError

```
错误：ModuleNotFoundError: No module named 'xxx'
解决：
conda activate trading_agents
pip install xxx
```

### 错误2：OpenAI API错误

```
错误：AuthenticationError: Incorrect API key
解决：检查.env文件或config.py中的API密钥是否正确
```

### 错误3：yfinance下载数据失败

```
错误：No data found, symbol may be delisted
解决：
1. 检查网络连接
2. 尝试其他股票代码（如MSFT, GOOGL）
3. 检查日期范围是否合理（不要选择未来日期）
```

### 错误4：内存不足

```
错误：MemoryError
解决：
1. 减少测试的股票数量
2. 缩短日期范围
3. 关闭其他占用内存的程序
```

### 错误5：API速率限制

```
错误：Rate limit exceeded
解决：
1. 程序会自动重试，请等待
2. 减少并发请求（修改代码中的sleep时间）
3. 升级OpenAI API套餐
```

## 性能优化建议

1. **首次运行**：建议先用1个月数据测试，确保流程正常
2. **缓存数据**：下载的股票数据可以保存，避免重复下载
3. **并行处理**：如果测试多个股票，可以考虑并行处理
4. **使用更快的模型**：gpt-3.5-turbo比gpt-4快且便宜

## 估算运行时间和成本

### 运行时间（1年数据，1个股票）
- 数据收集：1-2分钟
- Agent分析：30-60分钟（取决于模型）
- 总计：约1小时

### API成本估算（1年数据，1个股票）
- 使用GPT-4：约$10-20
- 使用GPT-3.5-turbo：约$1-3

## 下一步

1. 查看`README.md`了解项目详细文档
2. 阅读`experiments/`目录下的实验脚本
3. 根据需要修改Agent的Prompt（在`prompts/prompt_templates.py`）
4. 自定义评估指标（在`evaluation/metrics.py`）

## 获取帮助

如果遇到问题：
1. 检查错误信息，参考上面的"常见错误及解决方案"
2. 查看项目的README.md中的"常见问题"部分
3. 检查API密钥是否有效且有足够余额
4. 确认网络连接正常

## 退出环境

完成工作后，可以退出conda环境：

```bash
conda deactivate
```

下次使用时，只需：

```bash
conda activate trading_agents
cd /path/to/trading_agents_project
python experiments/baseline_simple.py
```

---

**祝你使用顺利！如有问题，请参考README.md或检查错误日志。**
