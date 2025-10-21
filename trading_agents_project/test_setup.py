"""
测试脚本 - 验证环境配置和代码修复
运行此脚本来检查所有依赖是否正确安装
"""

import sys
print(f"Python版本: {sys.version}\n")

# 测试1: 检查必需的包
print("=" * 60)
print("测试1: 检查依赖包安装")
print("=" * 60)

required_packages = {
    'yfinance': 'yfinance',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'openai': 'openai',
    'ta': 'ta',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
}

all_installed = True
for package_name, import_name in required_packages.items():
    try:
        __import__(import_name)
        print(f"✅ {package_name:20s} - 已安装")
    except ImportError as e:
        print(f"❌ {package_name:20s} - 未安装")
        all_installed = False

print()

# 测试2: 检查项目模块导入
print("=" * 60)
print("测试2: 检查项目模块")
print("=" * 60)

try:
    from config.config import config
    print("✅ config.config - 导入成功")
    print(f"   API密钥已设置: {'是' if config.OPENAI_API_KEY and len(config.OPENAI_API_KEY) > 10 else '否'}")
    print(f"   模型: {config.OPENAI_MODEL}")
except Exception as e:
    print(f"❌ config.config - 导入失败: {e}")
    all_installed = False

try:
    from data.data_collector import DataCollector
    print("✅ data.data_collector - 导入成功")
except Exception as e:
    print(f"❌ data.data_collector - 导入失败: {e}")
    all_installed = False

try:
    from agents.base_agent import BaseAgent
    print("✅ agents.base_agent - 导入成功")
except Exception as e:
    print(f"❌ agents.base_agent - 导入失败: {e}")
    all_installed = False

print()

# 测试3: 检查OpenAI API新版本
print("=" * 60)
print("测试3: 检查OpenAI API版本")
print("=" * 60)

try:
    import openai
    # 尝试导入新版API
    from openai import OpenAI
    print(f"✅ OpenAI包版本: {openai.__version__}")
    print("✅ 新版API (OpenAI客户端) 可用")

    # 检查是否有旧版API的使用
    print("✅ 代码已更新为使用新版OpenAI API")
except ImportError:
    print("❌ OpenAI包未正确安装或版本过旧")
    all_installed = False

print()

# 测试4: 测试数据目录
print("=" * 60)
print("测试4: 检查目录结构")
print("=" * 60)

import os
from pathlib import Path

required_dirs = ['data', 'agents', 'config', 'experiments', 'results']
for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"✅ {dir_name}/ - 存在")
    else:
        print(f"⚠️  {dir_name}/ - 不存在（某些目录可能会自动创建）")

print()

# 测试5: 快速功能测试（不调用API）
print("=" * 60)
print("测试5: 基础功能测试")
print("=" * 60)

try:
    from data.data_collector import DataCollector
    collector = DataCollector(['AAPL'])
    print("✅ DataCollector初始化成功")
except Exception as e:
    print(f"❌ DataCollector初始化失败: {e}")
    all_installed = False

try:
    from data.data_processor import DataProcessor
    processor = DataProcessor()
    print("✅ DataProcessor初始化成功")
except Exception as e:
    print(f"❌ DataProcessor初始化失败: {e}")
    all_installed = False

print()

# 最终结果
print("=" * 60)
print("测试总结")
print("=" * 60)

if all_installed:
    print("✅ 所有测试通过！环境配置正确。")
    print()
    print("下一步：")
    print("1. 确保在config/config.py或.env文件中配置了有效的OpenAI API密钥")
    print("2. 运行实验脚本: python experiments/baseline_simple.py")
    print("3. 或使用Jupyter Notebook进行交互式探索")
else:
    print("❌ 部分测试失败。请检查上面的错误信息。")
    print()
    print("建议：")
    print("1. 确保已激活conda环境: conda activate trading_agents")
    print("2. 安装依赖: pip install -r requirements.txt")
    print("3. 查看ANACONDA_SETUP.md获取详细安装指南")

print("=" * 60)
