"""
Baseline 3: 简单模板Prompt方法
每个Agent有不同角色名称，但Prompt结构相同
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from typing import Dict
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


class SimpleTemplateAgent(BaseAgent):
    """使用简单模板Prompt的Agent"""
    
    def __init__(self, role_name: str, agent_type: str, api_key: str = None):
        """
        初始化Agent
        
        Args:
            role_name: 显示名称
            agent_type: Agent类型（用于区分不同的简单提示）
            api_key: API密钥
        """
        super().__init__(role_name=role_name, api_key=api_key)
        self.agent_type = agent_type
    
    def get_system_prompt(self) -> str:
        """简单的模板Prompt，只有角色名称不同"""
        role_descriptions = {
            'fundamental': '基本面分析师',
            'technical': '技术分析师',
            'sentiment': '情绪分析师',
            'news': '新闻分析师'
        }
        
        role = role_descriptions.get(self.agent_type, '分析师')
        
        return f"""你是一名{role}，请根据以下信息给出分析。

请给出你的专业判断，并说明理由。

输出格式要求：
{{
    "agent": "{role}",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "你的分析理由"
}}
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化输入数据（根据Agent类型略有不同）"""
        symbol = data.get('symbol', 'Unknown')
        prompt = f"请分析 {symbol} 股票：\n\n"
        
        # 根据Agent类型选择关注的数据
        if self.agent_type == 'fundamental':
            if 'financial_data' in data:
                prompt += f"财务数据: {data['financial_data']}\n"
        
        elif self.agent_type == 'technical':
            if 'technical_summary' in data:
                prompt += f"技术指标: {data['technical_summary']}\n"
        
        elif self.agent_type == 'sentiment':
            if 'sentiment_data' in data:
                prompt += f"市场情绪: {data['sentiment_data']}\n"
        
        elif self.agent_type == 'news':
            if 'news_data' in data:
                prompt += f"近期新闻: {data['news_data']}\n"
        
        prompt += "\n请给出你的分析。"
        
        return prompt


class BaselineSimpleExperiment:
    """简单模板Prompt实验类"""
    
    def __init__(self, symbol: str = 'AAPL'):
        """初始化实验"""
        self.symbol = symbol
        self.data_collector = DataCollector([symbol])
        self.data_processor = DataProcessor()
        
        # 创建使用简单模板的Agents
        self.agents = {
            'fundamental': SimpleTemplateAgent('Fundamental', 'fundamental'),
            'technical': SimpleTemplateAgent('Technical', 'technical'),
            'sentiment': SimpleTemplateAgent('Sentiment', 'sentiment'),
            'news': SimpleTemplateAgent('News', 'news'),
        }
        
    def collect_data(self, start_date: str, end_date: str):
        """收集数据"""
        print(f"\n{'='*60}")
        print(f"收集 {self.symbol} 的数据")
        print(f"{'='*60}\n")
        
        all_data = self.data_collector.collect_all_data(
            self.symbol, start_date, end_date
        )
        
        price_data = all_data['price_data']
        price_data = self.data_processor.calculate_technical_indicators(price_data)
        all_data['price_data'] = price_data
        
        return all_data
    
    def run_daily_analysis(self, date: str, data: Dict) -> Dict:
        """运行单日分析"""
        tech_summary = self.data_processor.generate_technical_summary(
            data['price_data'], date
        )
        
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
        
        # 综合决策
        stances = [a.get('stance', 'neutral') for a in analyses.values()]
        confidences = [a.get('confidence', 0.5) for a in analyses.values()]
        
        from collections import Counter
        stance_counts = Counter(stances)
        final_stance = stance_counts.most_common(1)[0][0]
        
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
        """运行完整实验（支持训练/测试划分）"""
        print(f"\n{'='*60}")
        print(f"开始运行 Baseline Simple Template 实验")
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
        common_dates = results_df.index.intersection(actual_returns.index)
        results_df = results_df.loc[common_dates]
        actual_returns = actual_returns.loc[common_dates]
        
        # 评估策略
        metrics = evaluate_strategy(
            results_df[['signal']].rename(columns={'signal': 'signal'}),
            actual_returns,
            config.RISK_FREE_RATE
        )
        
        metrics['avg_consistency'] = results_df['consistency'].mean()
        metrics['avg_confidence'] = results_df['final_confidence'].mean()
        
        # 保存结果
        experiment_results = {
            'experiment_name': 'baseline_simple',
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

        if config.USE_TRAIN_TEST_SPLIT:
            print_results_table(metrics, f"Baseline Simple Template 实验结果 (仅测试集: {config.TEST_START_DATE} 到 {config.TEST_END_DATE})")
        else:
            print_results_table(metrics, "Baseline Simple Template 实验结果 (全部数据)")

        save_results(experiment_results, 'baseline_simple', config.RESULTS_DIR)

        return experiment_results


def main():
    """主函数"""
    experiment = BaselineSimpleExperiment(symbol='AAPL')
    
    results = experiment.run_experiment(
        start_date=config.START_DATE,
        end_date=config.END_DATE
    )
    
    print("\n✅ 实验完成!")


if __name__ == "__main__":
    main()