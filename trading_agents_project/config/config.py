"""
配置文件
包含API密钥、数据路径、模型参数等配置
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """系统配置类"""
    
    # ==================== 项目路径 ====================
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data" / "raw"
    PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
    RESULTS_DIR = BASE_DIR / "results"
    
    # 创建必要的目录
    for dir_path in [DATA_DIR, PROCESSED_DATA_DIR, RESULTS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # ==================== API配置 ====================
    # OpenAI API (用于LLM调用)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")  # 请设置环境变量或直接替换此处
    OPENAI_MODEL = "gpt-4"  # 或 "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 2000
    
    # News API (用于获取新闻数据) - 可选
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your-news-api-key")
    
    # ==================== 股票数据配置 ====================
    # 目标股票列表
    STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    # 数据时间范围
    START_DATE = "2022-01-01"
    END_DATE = "2024-10-01"
    
    # 训练/测试划分
    TRAIN_TEST_SPLIT = 0.8  # 80%训练，20%测试
    
    # ==================== 技术指标配置 ====================
    TECHNICAL_INDICATORS = {
        'SMA_SHORT': 20,      # 短期移动平均
        'SMA_LONG': 50,       # 长期移动平均
        'RSI_PERIOD': 14,     # RSI周期
        'MACD_FAST': 12,      # MACD快线
        'MACD_SLOW': 26,      # MACD慢线
        'MACD_SIGNAL': 9,     # MACD信号线
        'BB_PERIOD': 20,      # 布林带周期
        'BB_STD': 2,          # 布林带标准差
    }
    
    # ==================== 交易策略配置 ====================
    INITIAL_CAPITAL = 100000  # 初始资金
    POSITION_SIZE = 0.1       # 每次交易仓位(10%)
    STOP_LOSS = 0.05          # 止损比例(5%)
    TAKE_PROFIT = 0.15        # 止盈比例(15%)
    
    # ==================== Agent配置 ====================
    AGENT_TEMPERATURE = 0.7   # Agent决策温度
    MAX_RETRIES = 3           # API调用最大重试次数
    
    # ==================== 实验配置 ====================
    NUM_RUNS = 5              # 每个方案运行次数(减少随机性)
    RANDOM_SEED = 42          # 随机种子
    
    # ==================== 评估指标配置 ====================
    RISK_FREE_RATE = 0.02     # 无风险利率(年化2%)

# 创建全局配置实例
config = Config()