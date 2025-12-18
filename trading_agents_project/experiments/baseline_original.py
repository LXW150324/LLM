"""
Baseline 1: 原始TradingAgents方法
所有Agent使用相同的通用Prompt
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

from config.config import config
from data.data_collector import DataCollector
from data.data_processor import DataProcessor
from agents.base_agent import BaseAgent
from evaluation.metrics import evaluate_strategy, ConsistencyMetrics
from utils.helpers import (
    save_results, print_results_table, 
    get_signal_from_stance, ProgressTracker
)


class OriginalPromptAgent(BaseAgent):
    """使用原始通用Prompt的Agent"""
    
    def __init__(self, role_name: str, api_key: str = None):
        super().__init__(role_name=role_name, api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """所有Agent使用相同的通用Prompt"""
        return """你是一位专业的金融分析师。请分析提供的数据并给出你对股票的判断。

请基于数据进行分析，并给出你的观点（看多/看空/中性）以及理由。

输出格式要求：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "你的分析理由"
}
"""
    
    def format_input_data(self, data: Dict) -> str:
        """简单地将所有数据转换为文本"""
        symbol = data.get('symbol', 'Unknown')
        
        # 简单格式化所有可用数据
        prompt = f"请分析 {symbol} 股票的以下数据：\n\n"
        
        # 价格数据
        if 'current_price' in data:
            prompt += f"当前价格: ${data['current_price']:.2f}\n"
        
        # 技术数据
        if 'technical_summary' in data:
            tech = data['technical_summary']
            prompt += f"\n技术指标: {tech}\n"
        
        # 财务数据
        if 'financial_data' in data:
            fin = data['financial_data']
            prompt += f"\n财务数据: {fin}\n"
        
        # 新闻数据
        if 'news_data' in data:
            news = data['news_data']
            prompt += f"\n近期新闻: {news}\n"
        
        # 情绪数据
        if 'sentiment_data' in data:
            sent = data['sentiment_data']
            prompt += f"\n市场情绪: {sent}\n"
        
        prompt += "\n请给出你的分析和判断。"
        
        return prompt


class BaselineOriginalExperiment:
    """原始Prompt方法的实验类"""
    
    def __init__(self, symbol: str = 'AAPL'):
        """
        初始化实验
        
        Args:
            symbol: 股票代码
        """
        self.symbol = symbol
        self.data_collector = DataCollector([symbol])
        self.data_processor = DataProcessor()
        
        # 创建使用原始Prompt的Agents
        self.agents = {
            'fundamental': OriginalPromptAgent('Analyst'),
            'technical': OriginalPromptAgent('Analyst'),
            'sentiment': OriginalPromptAgent('Analyst'),
            'news': OriginalPromptAgent('Analyst'),
        }
        
        self.results = []
        
    def collect_data(self, start_date: str, end_date: str):
        """收集数据"""
        print(f"\n{'='*60}")
        print(f"收集 {self.symbol} 的数据")
        print(f"{'='*60}\n")
        
        # 收集所有数据
        all_data = self.data_collector.collect_all_data(
            self.symbol, start_date, end_date
        )
        
        # 处理价格数据并计算技术指标
        price_data = all_data['price_data']
        price_data = self.data_processor.calculate_technical_indicators(price_data)
        
        all_data['price_data'] = price_data
        
        return all_data
    
    def run_daily_analysis(self, date: str, data: Dict) -> Dict:
        """
        运行单日分析
        
        Args:
            date: 日期
            data: 当日数据
            
        Returns:
            分析结果
        """
        # 获取技术指标摘要
        tech_summary = self.data_processor.generate_technical_summary(
            data['price_data'], date
        )
        
        # 准备输入数据
        input_data = {
            'symbol': self.symbol,
            'current_price': tech_summary['price']['current'],
            'technical_summary': tech_summary,
            'financial_data': data['financial_data'],
            'news_data': data['news_data'],
            'sentiment_data': data['sentiment_data']
        }
        
        # 收集所有Agent的分析
        analyses = {}
        for agent_name, agent in self.agents.items():
            try:
                analysis = agent.analyze(input_data)
                analyses[agent_name] = analysis
            except Exception as e:
                print(f"⚠️  {agent_name} 分析失败: {str(e)}")
                analyses[agent_name] = {
                    'stance': 'neutral',
                    'confidence': 0.5,
                    'reasoning': 'Analysis failed'
                }
        
        # 综合决策（简单投票）
        stances = [a.get('stance', 'neutral') for a in analyses.values()]
        confidences = [a.get('confidence', 0.5) for a in analyses.values()]
        
        # 统计立场
        from collections import Counter
        stance_counts = Counter(stances)
        final_stance = stance_counts.most_common(1)[0][0]
        
        # 计算一致性
        consistency = ConsistencyMetrics.calculate_stance_agreement(stances)
        
        return {
            'date': date,
            'symbol': self.symbol,
            'price': tech_summary['price']['current'],
            'analyses': analyses,
            'final_stance': final_stance,
            'final_confidence': np.mean(confidences),
            'consistency': consistency,
            'signal': get_signal_from_stance(final_stance)
        }
    
    def run_experiment(self, start_date: str, end_date: str) -> Dict:
        """
        运行完整实验（支持训练/测试划分）

        Args:
            start_date: 开始日期
            end_date: 结束日期

        Returns:
            实验结果
        """
        print(f"\n{'='*60}")
        print(f"开始运行 Baseline Original 实验")
        print(f"股票: {self.symbol}")
        print(f"时间: {start_date} 到 {end_date}")

        if config.USE_TRAIN_TEST_SPLIT:
            print(f"🔥 使用严格训练/测试划分模式:")
            print(f"   训练集: {start_date} 到 {config.TRAIN_END_DATE}")
            print(f"   测试集: {config.TEST_START_DATE} 到 {config.TEST_END_DATE}")
            print(f"   ⚠️  只在测试集上评估性能！")
        print(f"{'='*60}\n")

        # 收集完整数据
        all_data = self.collect_data(start_date, end_date)
        price_data = all_data['price_data']

        # 获取所有交易日期
        all_trading_dates = price_data.index.strftime('%Y-%m-%d').tolist()

        # 划分训练集和测试集日期
        if config.USE_TRAIN_TEST_SPLIT:
            test_dates = [d for d in all_trading_dates
                         if config.TEST_START_DATE <= d <= config.TEST_END_DATE]
            dates_to_analyze = test_dates
            print(f"📊 测试集: {len(test_dates)} 天\n")
        else:
            dates_to_analyze = all_trading_dates

        # 运行每日分析
        daily_results = []

        with ProgressTracker(len(dates_to_analyze), "分析进度") as tracker:
            for date in dates_to_analyze:
                result = self.run_daily_analysis(date, all_data)
                daily_results.append(result)
                tracker.update()
        
        # 转换为DataFrame
        results_df = pd.DataFrame(daily_results)
        results_df['date'] = pd.to_datetime(results_df['date'])
        results_df = results_df.set_index('date')
        
        # 计算性能指标
        actual_returns = price_data['returns']
        
        # 对齐索引
        common_dates = results_df.index.intersection(actual_returns.index)
        results_df = results_df.loc[common_dates]
        actual_returns = actual_returns.loc[common_dates]
        
        # 评估策略
        metrics = evaluate_strategy(
            results_df[['signal']].rename(columns={'signal': 'signal'}),
            actual_returns,
            config.RISK_FREE_RATE
        )
        
        # 添加一致性指标
        metrics['avg_consistency'] = results_df['consistency'].mean()
        metrics['avg_confidence'] = results_df['final_confidence'].mean()
        
        # 保存结果
        experiment_results = {
            'experiment_name': 'baseline_original',
            'symbol': self.symbol,
            'start_date': start_date,
            'end_date': end_date,
            'use_train_test_split': config.USE_TRAIN_TEST_SPLIT,
            'train_end_date': config.TRAIN_END_DATE if config.USE_TRAIN_TEST_SPLIT else None,
            'test_start_date': config.TEST_START_DATE if config.USE_TRAIN_TEST_SPLIT else None,
            'test_end_date': config.TEST_END_DATE if config.USE_TRAIN_TEST_SPLIT else None,
            'num_test_days': len(results_df) if config.USE_TRAIN_TEST_SPLIT else None,
            'metrics': metrics,
            'daily_results': results_df.to_dict('records')
        }

        # 打印结果
        if config.USE_TRAIN_TEST_SPLIT:
            print_results_table(metrics, f"Baseline Original 实验结果 (仅测试集: {config.TEST_START_DATE} 到 {config.TEST_END_DATE})")
        else:
            print_results_table(metrics, "Baseline Original 实验结果 (全部数据)")

        # 保存到文件
        save_results(experiment_results, 'baseline_original', config.RESULTS_DIR)

        return experiment_results


def main():
    """主函数"""
    # 运行实验
    experiment = BaselineOriginalExperiment(symbol='AAPL')
    
    results = experiment.run_experiment(
        start_date=config.START_DATE,
        end_date=config.END_DATE
    )
    
    print("\n✅ 实验完成!")
    

if __name__ == "__main__":
    main()