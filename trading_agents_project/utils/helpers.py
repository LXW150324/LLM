"""
辅助工具函数
"""

import json
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import logging

def setup_logging(log_file: str = None, level: int = logging.INFO):
    """
    设置日志
    
    Args:
        log_file: 日志文件路径
        level: 日志级别
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=level, format=log_format)
    
    return logging.getLogger(__name__)


def save_json(data: Dict, filepath: str):
    """
    保存JSON文件
    
    Args:
        data: 要保存的数据
        filepath: 文件路径
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ 已保存到: {filepath}")


def load_json(filepath: str) -> Dict:
    """
    加载JSON文件
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def save_pickle(data: Any, filepath: str):
    """
    保存Pickle文件
    
    Args:
        data: 要保存的数据
        filepath: 文件路径
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
    
    print(f"✅ 已保存到: {filepath}")


def load_pickle(filepath: str) -> Any:
    """
    加载Pickle文件
    
    Args:
        filepath: 文件路径
        
    Returns:
        加载的数据
    """
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    
    return data


def save_results(results: Dict, experiment_name: str, results_dir: str = "results"):
    """
    保存实验结果
    
    Args:
        results: 结果字典
        experiment_name: 实验名称
        results_dir: 结果目录
    """
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # 添加时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{experiment_name}_{timestamp}.json"
    
    filepath = results_dir / filename
    save_json(results, filepath)
    
    return filepath


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    格式化百分比
    
    Args:
        value: 数值
        decimals: 小数位数
        
    Returns:
        格式化的字符串
    """
    return f"{value * 100:.{decimals}f}%"


def format_currency(value: float, decimals: int = 2) -> str:
    """
    格式化货币
    
    Args:
        value: 数值
        decimals: 小数位数
        
    Returns:
        格式化的字符串
    """
    return f"${value:,.{decimals}f}"


def print_results_table(results: Dict, title: str = "Results"):
    """
    打印结果表格
    
    Args:
        results: 结果字典
        title: 表格标题
    """
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")
    
    for key, value in results.items():
        key_display = key.replace('_', ' ').title()
        
        if isinstance(value, float):
            if 'return' in key or 'rate' in key or 'ratio' in key:
                value_display = f"{value:.4f}"
            elif 'accuracy' in key:
                value_display = format_percentage(value)
            else:
                value_display = f"{value:.4f}"
        else:
            value_display = str(value)
        
        print(f"{key_display:<40} {value_display:>18}")
    
    print(f"{'='*60}\n")


def compare_results(results_dict: Dict[str, Dict], metric_names: List[str] = None):
    """
    比较多个实验结果
    
    Args:
        results_dict: {实验名称: 结果字典}
        metric_names: 要比较的指标名称列表
    """
    if metric_names is None:
        # 使用第一个结果的所有指标
        metric_names = list(next(iter(results_dict.values())).keys())
    
    # 创建比较表格
    comparison = {}
    for metric in metric_names:
        comparison[metric] = {
            name: results.get(metric, 'N/A')
            for name, results in results_dict.items()
        }
    
    # 转换为DataFrame
    df = pd.DataFrame(comparison).T
    
    print(f"\n{'='*80}")
    print(f"{'实验结果对比':^80}")
    print(f"{'='*80}")
    print(df.to_string())
    print(f"{'='*80}\n")
    
    return df


def create_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    创建摘要统计
    
    Args:
        df: 数据DataFrame
        
    Returns:
        摘要统计DataFrame
    """
    summary = df.describe()
    
    # 添加额外的统计量
    summary.loc['skewness'] = df.skew()
    summary.loc['kurtosis'] = df.kurtosis()
    
    return summary


def split_train_test(
    data: pd.DataFrame,
    train_ratio: float = 0.8,
    date_column: str = None
) -> tuple:
    """
    划分训练集和测试集
    
    Args:
        data: 数据DataFrame
        train_ratio: 训练集比例
        date_column: 日期列名（如果需要按日期排序）
        
    Returns:
        (训练集, 测试集)
    """
    if date_column and date_column in data.columns:
        data = data.sort_values(date_column)
    
    split_idx = int(len(data) * train_ratio)
    
    train_data = data.iloc[:split_idx].copy()
    test_data = data.iloc[split_idx:].copy()
    
    print(f"训练集大小: {len(train_data)}")
    print(f"测试集大小: {len(test_data)}")
    
    return train_data, test_data


def calculate_portfolio_value(
    initial_capital: float,
    signals: np.ndarray,
    returns: np.ndarray,
    position_size: float = 1.0
) -> pd.Series:
    """
    计算投资组合价值变化
    
    Args:
        initial_capital: 初始资金
        signals: 交易信号
        returns: 收益率
        position_size: 仓位大小
        
    Returns:
        投资组合价值序列
    """
    # 将信号转换为持仓
    positions = np.zeros_like(signals)
    positions[1:] = signals[:-1]
    
    # 策略收益
    strategy_returns = positions * returns * position_size
    
    # 计算累计价值
    portfolio_value = initial_capital * np.cumprod(1 + strategy_returns)
    
    return pd.Series(portfolio_value)


def get_signal_from_stance(stance: str) -> int:
    """
    将立场转换为交易信号
    
    Args:
        stance: 立场 ('bullish', 'bearish', 'neutral')
        
    Returns:
        信号 (1, -1, 0)
    """
    stance_map = {
        'bullish': 1,
        'bearish': -1,
        'neutral': 0,
        'buy': 1,
        'sell': -1,
        'hold': 0
    }
    
    return stance_map.get(stance.lower(), 0)


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total: int, description: str = "Processing"):
        """
        初始化进度跟踪器
        
        Args:
            total: 总步骤数
            description: 描述
        """
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = datetime.now()
    
    def update(self, step: int = 1):
        """更新进度"""
        self.current += step
        percentage = (self.current / self.total) * 100
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"{eta:.0f}s"
        else:
            eta_str = "N/A"
        
        print(f"\r{self.description}: {self.current}/{self.total} "
              f"({percentage:.1f}%) - ETA: {eta_str}", end='')
        
        if self.current >= self.total:
            print()  # 换行
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.current < self.total:
            print()  # 确保换行