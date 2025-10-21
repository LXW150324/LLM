"""
评估指标模块
计算各种性能指标
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from scipy import stats

class TradingMetrics:
    """交易性能指标计算器"""
    
    @staticmethod
    def calculate_accuracy(predictions: np.ndarray, actuals: np.ndarray) -> float:
        """
        计算趋势预测准确率
        
        Args:
            predictions: 预测的方向 (1=上涨, 0=下跌)
            actuals: 实际的方向 (1=上涨, 0=下跌)
            
        Returns:
            准确率 (0-1)
        """
        if len(predictions) == 0:
            return 0.0
        
        correct = np.sum(predictions == actuals)
        total = len(predictions)
        
        return correct / total
    
    @staticmethod
    def calculate_returns(
        signals: np.ndarray,
        price_returns: np.ndarray,
        position_size: float = 1.0
    ) -> np.ndarray:
        """
        计算策略收益序列
        
        Args:
            signals: 交易信号 (1=买入, -1=卖出, 0=持有)
            price_returns: 价格收益率序列
            position_size: 仓位大小
            
        Returns:
            策略收益序列
        """
        # 将信号转换为持仓（前一天的信号决定今天的持仓）
        positions = np.zeros_like(signals)
        positions[1:] = signals[:-1]
        
        # 策略收益 = 持仓 * 价格收益 * 仓位大小
        strategy_returns = positions * price_returns * position_size
        
        return strategy_returns
    
    @staticmethod
    def calculate_cumulative_returns(returns: np.ndarray) -> np.ndarray:
        """
        计算累计收益
        
        Args:
            returns: 收益序列
            
        Returns:
            累计收益序列
        """
        return np.cumprod(1 + returns) - 1
    
    @staticmethod
    def calculate_total_return(returns: np.ndarray) -> float:
        """
        计算总收益率
        
        Args:
            returns: 收益序列
            
        Returns:
            总收益率
        """
        return np.prod(1 + returns) - 1
    
    @staticmethod
    def calculate_annualized_return(returns: np.ndarray, periods_per_year: int = 252) -> float:
        """
        计算年化收益率
        
        Args:
            returns: 收益序列
            periods_per_year: 每年的交易周期数（股票通常为252天）
            
        Returns:
            年化收益率
        """
        total_return = TradingMetrics.calculate_total_return(returns)
        n_periods = len(returns)
        
        if n_periods == 0:
            return 0.0
        
        annualized = (1 + total_return) ** (periods_per_year / n_periods) - 1
        
        return annualized
    
    @staticmethod
    def calculate_sharpe_ratio(
        returns: np.ndarray,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """
        计算夏普比率
        
        Args:
            returns: 收益序列
            risk_free_rate: 无风险利率（年化）
            periods_per_year: 每年的交易周期数
            
        Returns:
            夏普比率
        """
        if len(returns) == 0 or np.std(returns) == 0:
            return 0.0
        
        # 日均收益
        mean_return = np.mean(returns)
        
        # 日无风险收益
        daily_rf = risk_free_rate / periods_per_year
        
        # 超额收益
        excess_return = mean_return - daily_rf
        
        # 收益标准差
        std_return = np.std(returns, ddof=1)
        
        # 年化夏普比率
        sharpe = (excess_return / std_return) * np.sqrt(periods_per_year)
        
        return sharpe
    
    @staticmethod
    def calculate_max_drawdown(returns: np.ndarray) -> Tuple[float, int, int]:
        """
        计算最大回撤
        
        Args:
            returns: 收益序列
            
        Returns:
            (最大回撤, 回撤开始位置, 回撤结束位置)
        """
        if len(returns) == 0:
            return 0.0, 0, 0
        
        # 计算累计收益曲线
        cumulative = np.cumprod(1 + returns)
        
        # 计算历史最高点
        running_max = np.maximum.accumulate(cumulative)
        
        # 计算回撤
        drawdown = (cumulative - running_max) / running_max
        
        # 找到最大回撤
        max_dd = np.min(drawdown)
        max_dd_idx = np.argmin(drawdown)
        
        # 找到回撤开始点（最大回撤前的最高点）
        start_idx = np.argmax(cumulative[:max_dd_idx+1])
        
        return abs(max_dd), start_idx, max_dd_idx
    
    @staticmethod
    def calculate_win_rate(returns: np.ndarray) -> float:
        """
        计算胜率（盈利交易占比）
        
        Args:
            returns: 收益序列
            
        Returns:
            胜率 (0-1)
        """
        if len(returns) == 0:
            return 0.0
        
        # 只统计有交易的时期（非零收益）
        trades = returns[returns != 0]
        
        if len(trades) == 0:
            return 0.0
        
        winning_trades = np.sum(trades > 0)
        total_trades = len(trades)
        
        return winning_trades / total_trades
    
    @staticmethod
    def calculate_profit_factor(returns: np.ndarray) -> float:
        """
        计算盈亏比（总盈利/总亏损）
        
        Args:
            returns: 收益序列
            
        Returns:
            盈亏比
        """
        gains = returns[returns > 0].sum()
        losses = abs(returns[returns < 0].sum())
        
        if losses == 0:
            return float('inf') if gains > 0 else 0.0
        
        return gains / losses
    
    @staticmethod
    def calculate_sortino_ratio(
        returns: np.ndarray,
        risk_free_rate: float = 0.02,
        periods_per_year: int = 252
    ) -> float:
        """
        计算索提诺比率（只考虑下行波动）
        
        Args:
            returns: 收益序列
            risk_free_rate: 无风险利率
            periods_per_year: 每年交易周期数
            
        Returns:
            索提诺比率
        """
        if len(returns) == 0:
            return 0.0
        
        mean_return = np.mean(returns)
        daily_rf = risk_free_rate / periods_per_year
        excess_return = mean_return - daily_rf
        
        # 只计算负收益的标准差（下行风险）
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0:
            return float('inf') if excess_return > 0 else 0.0
        
        downside_std = np.std(downside_returns, ddof=1)
        
        if downside_std == 0:
            return 0.0
        
        sortino = (excess_return / downside_std) * np.sqrt(periods_per_year)
        
        return sortino


class ConsistencyMetrics:
    """一致性指标计算器"""
    
    @staticmethod
    def calculate_stance_agreement(stances: List[str]) -> float:
        """
        计算多个Agent立场的一致性
        
        Args:
            stances: Agent立场列表 ['bullish', 'bearish', 'neutral', ...]
            
        Returns:
            一致性得分 (0-1)，1表示完全一致
        """
        if len(stances) <= 1:
            return 1.0
        
        # 统计每种立场的数量
        from collections import Counter
        stance_counts = Counter(stances)
        
        # 最多的立场数量
        max_count = max(stance_counts.values())
        
        # 一致性 = 最多立场数 / 总数
        agreement = max_count / len(stances)
        
        return agreement
    
    @staticmethod
    def calculate_confidence_variance(confidences: List[float]) -> float:
        """
        计算信心度的方差（离散度）
        
        Args:
            confidences: 信心度列表
            
        Returns:
            方差（越小表示越一致）
        """
        if len(confidences) <= 1:
            return 0.0
        
        return np.var(confidences, ddof=1)
    
    @staticmethod
    def calculate_decision_stability(decisions: np.ndarray) -> float:
        """
        计算决策稳定性（多次运行的一致性）
        
        Args:
            decisions: 多次运行的决策矩阵 (n_runs x n_days)
            
        Returns:
            稳定性得分 (0-1)
        """
        if decisions.shape[0] <= 1:
            return 1.0
        
        # 计算每天决策的一致性
        n_days = decisions.shape[1]
        daily_consistency = []
        
        for day in range(n_days):
            day_decisions = decisions[:, day]
            # 最多的决策数量 / 总运行次数
            from collections import Counter
            counts = Counter(day_decisions)
            max_count = max(counts.values())
            consistency = max_count / len(day_decisions)
            daily_consistency.append(consistency)
        
        # 平均一致性
        return np.mean(daily_consistency)


class ExplainabilityMetrics:
    """可解释性指标计算器"""
    
    @staticmethod
    def count_reasoning_length(reasoning_text: str) -> int:
        """
        统计理由文本的长度（单词数）
        
        Args:
            reasoning_text: 理由文本
            
        Returns:
            单词数
        """
        return len(reasoning_text.split())
    
    @staticmethod
    def count_evidence_citations(response_text: str) -> int:
        """
        统计证据引用次数
        
        Args:
            response_text: 响应文本
            
        Returns:
            引用次数
        """
        # 简单统计包含数字、百分比、指标名称的次数
        evidence_keywords = [
            'pe', 'pb', 'roe', 'rsi', 'macd', 'sma', '%', 
            '比率', '指标', '数据', '显示', '根据'
        ]
        
        text_lower = response_text.lower()
        citations = sum(1 for keyword in evidence_keywords if keyword in text_lower)
        
        return citations
    
    @staticmethod
    def calculate_explanation_score(
        reasoning_text: str,
        min_length: int = 50,
        min_citations: int = 2
    ) -> float:
        """
        计算解释性综合得分
        
        Args:
            reasoning_text: 理由文本
            min_length: 最小期望长度
            min_citations: 最小期望引用次数
            
        Returns:
            解释性得分 (0-1)
        """
        # 长度得分
        length = ExplainabilityMetrics.count_reasoning_length(reasoning_text)
        length_score = min(length / min_length, 1.0)
        
        # 引用得分
        citations = ExplainabilityMetrics.count_evidence_citations(reasoning_text)
        citation_score = min(citations / min_citations, 1.0)
        
        # 综合得分（加权平均）
        total_score = 0.6 * length_score + 0.4 * citation_score
        
        return total_score


def evaluate_strategy(
    predictions: pd.DataFrame,
    actual_returns: pd.Series,
    risk_free_rate: float = 0.02
) -> Dict:
    """
    综合评估策略性能
    
    Args:
        predictions: 预测结果DataFrame，包含'signal'列
        actual_returns: 实际收益率Series
        risk_free_rate: 无风险利率
        
    Returns:
        包含所有评估指标的字典
    """
    # 转换信号为数值
    signal_map = {'buy': 1, 'sell': -1, 'hold': 0, 
                  'bullish': 1, 'bearish': -1, 'neutral': 0}
    
    signals = predictions['signal'].map(signal_map).fillna(0).values
    returns = actual_returns.values
    
    # 计算策略收益
    strategy_returns = TradingMetrics.calculate_returns(signals, returns)
    
    # 计算所有指标
    metrics = {
        # 收益指标
        'total_return': TradingMetrics.calculate_total_return(strategy_returns),
        'annualized_return': TradingMetrics.calculate_annualized_return(strategy_returns),
        
        # 风险调整指标
        'sharpe_ratio': TradingMetrics.calculate_sharpe_ratio(strategy_returns, risk_free_rate),
        'sortino_ratio': TradingMetrics.calculate_sortino_ratio(strategy_returns, risk_free_rate),
        
        # 风险指标
        'max_drawdown': TradingMetrics.calculate_max_drawdown(strategy_returns)[0],
        'volatility': np.std(strategy_returns) * np.sqrt(252),
        
        # 交易指标
        'win_rate': TradingMetrics.calculate_win_rate(strategy_returns),
        'profit_factor': TradingMetrics.calculate_profit_factor(strategy_returns),
        
        # 预测指标
        'direction_accuracy': TradingMetrics.calculate_accuracy(
            (signals > 0).astype(int),
            (returns > 0).astype(int)
        ),
        
        # 交易统计
        'total_trades': np.sum(signals != 0),
        'avg_return_per_trade': np.mean(strategy_returns[strategy_returns != 0]) if np.any(strategy_returns != 0) else 0,
    }
    
    return metrics