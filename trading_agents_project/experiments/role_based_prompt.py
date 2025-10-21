"""
我们的方法: 基于角色定制的Prompt
为每个Agent设计专门的Prompt，包含角色定位、数据格式、输出要求
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

# 导入所有定制化的Agents
from agents.fundamental_agent import FundamentalAnalysisAgent
from agents.technical_agent import TechnicalAnalysisAgent
from agents.sentiment_agent import SentimentAnalysisAgent
from agents.news_agent import NewsAnalysisAgent
from agents.bull_bear_agent import BullResearcherAgent, BearResearcherAgent
from agents.risk_agent import RiskManagementAgent
from agents.trader_agent import TraderAgent

from evaluation.metrics import evaluate_strategy, ConsistencyMetrics, ExplainabilityMetrics
from utils.helpers import (
    save_results, print_results_table, 
    get_signal_from_stance, ProgressTracker
)


class RoleBasedPromptExperiment:
    """基于角色定制Prompt的完整实验"""
    
    def __init__(self, symbol: str = 'AAPL'):
        """初始化实验"""
        self.symbol = symbol
        self.data_collector = DataCollector([symbol])
        self.data_processor = DataProcessor()
        
        # 创建所有定制化的Agents
        self.fundamental_agent = FundamentalAnalysisAgent()
        self.technical_agent = TechnicalAnalysisAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.news_agent = NewsAnalysisAgent()
        self.bull_agent = BullResearcherAgent()
        self.bear_agent = BearResearcherAgent()
        self.risk_agent = RiskManagementAgent()
        self.trader_agent = TraderAgent()
        
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
        """
        运行单日的完整多Agent分析流程
        
        这是我们方法的核心：
        1. 各专业分析师并行分析
        2. 牛熊研究员辩论
        3. 风险管理评估
        4. 交易员最终决策
        """
        tech_summary = self.data_processor.generate_technical_summary(
            data['price_data'], date
        )
        
        current_price = tech_summary['price']['current']
        price_change = tech_summary['price']['change_pct']
        
        # ========== 阶段1: 专业分析师并行分析 ==========
        print(f"\n分析日期: {date}")
        print("  步骤1: 专业分析师分析...")
        
        # 基本面分析
        fundamental_input = {
            'symbol': self.symbol,
            'financial_data': data['financial_data'],
            'current_price': current_price
        }
        fundamental_analysis = self.fundamental_agent.analyze(fundamental_input)
        
        # 技术分析
        technical_input = {
            'symbol': self.symbol,
            'technical_summary': tech_summary
        }
        technical_analysis = self.technical_agent.analyze(technical_input)
        
        # 情绪分析
        sentiment_input = {
            'symbol': self.symbol,
            'sentiment_data': data['sentiment_data'],
            'current_price': current_price,
            'price_change': price_change
        }
        sentiment_analysis = self.sentiment_agent.analyze(sentiment_input)
        
        # 新闻分析
        news_input = {
            'symbol': self.symbol,
            'news_data': data['news_data'],
            'current_price': current_price
        }
        news_analysis = self.news_agent.analyze(news_input)
        
        # 收集所有分析报告
        analyst_reports = {
            'Fundamental Analyst': fundamental_analysis,
            'Technical Analyst': technical_analysis,
            'Sentiment Analyst': sentiment_analysis,
            'News Analyst': news_analysis
        }
        
        # ========== 阶段2: 牛熊研究员辩论 ==========
        print("  步骤2: 牛熊研究员辩论...")
        
        research_input = {
            'symbol': self.symbol,
            'analyst_reports': analyst_reports
        }
        
        bull_research = self.bull_agent.analyze(research_input)
        bear_research = self.bear_agent.analyze(research_input)
        
        # ========== 阶段3: 风险管理评估 ==========
        print("  步骤3: 风险管理评估...")
        
        # 综合所有分析得出初步决策倾向
        all_stances = [
            fundamental_analysis.get('stance', 'neutral'),
            technical_analysis.get('stance', 'neutral'),
            sentiment_analysis.get('stance', 'neutral'),
            news_analysis.get('stance', 'neutral')
        ]
        
        from collections import Counter
        stance_counts = Counter(all_stances)
        preliminary_action = stance_counts.most_common(1)[0][0]
        
        risk_input = {
            'symbol': self.symbol,
            'proposed_action': preliminary_action,
            'current_price': current_price,
            'proposed_position_size': config.POSITION_SIZE,
            'portfolio_value': config.INITIAL_CAPITAL,
            'analyst_reports': analyst_reports
        }
        
        risk_assessment = self.risk_agent.analyze(risk_input)
        
        # ========== 阶段4: 交易员最终决策 ==========
        print("  步骤4: 交易员最终决策...")
        
        trader_input = {
            'symbol': self.symbol,
            'current_price': current_price,
            'fundamental_analysis': fundamental_analysis,
            'technical_analysis': technical_analysis,
            'sentiment_analysis': sentiment_analysis,
            'news_analysis': news_analysis,
            'bull_research': bull_research,
            'bear_research': bear_research,
            'risk_assessment': risk_assessment
        }
        
        final_decision = self.trader_agent.analyze(trader_input)
        
        # ========== 计算评估指标 ==========
        
        # 一致性评分
        all_stances_extended = all_stances + [
            bull_research.get('stance', 'bullish'),
            bear_research.get('stance', 'bearish')
        ]
        consistency = ConsistencyMetrics.calculate_stance_agreement(all_stances_extended)
        
        # 信心度方差
        all_confidences = [
            fundamental_analysis.get('confidence', 0.5),
            technical_analysis.get('confidence', 0.5),
            sentiment_analysis.get('confidence', 0.5),
            news_analysis.get('confidence', 0.5)
        ]
        confidence_variance = ConsistencyMetrics.calculate_confidence_variance(all_confidences)
        
        # 可解释性评分
        all_reasoning = ' '.join([
            fundamental_analysis.get('reasoning', ''),
            technical_analysis.get('reasoning', ''),
            sentiment_analysis.get('reasoning', ''),
            news_analysis.get('reasoning', '')
        ])
        explainability_score = ExplainabilityMetrics.calculate_explanation_score(all_reasoning)
        
        return {
            'date': date,
            'symbol': self.symbol,
            'price': current_price,
            
            # 各分析师结果
            'fundamental_analysis': fundamental_analysis,
            'technical_analysis': technical_analysis,
            'sentiment_analysis': sentiment_analysis,
            'news_analysis': news_analysis,
            
            # 研究员辩论结果
            'bull_research': bull_research,
            'bear_research': bear_research,
            
            # 风险和决策
            'risk_assessment': risk_assessment,
            'final_decision': final_decision,
            
            # 综合指标
            'final_stance': final_decision.get('decision', 'hold'),
            'final_confidence': final_decision.get('confidence', 0.5),
            'consistency': consistency,
            'confidence_variance': confidence_variance,
            'explainability_score': explainability_score,
            'signal': get_signal_from_stance(final_decision.get('decision', 'hold'))
        }
    
    def run_experiment(self, start_date: str, end_date: str) -> Dict:
        """运行完整实验"""
        print(f"\n{'='*60}")
        print(f"开始运行 Role-Based Prompt 实验")
        print(f"股票: {self.symbol}")
        print(f"时间: {start_date} 到 {end_date}")
        print(f"{'='*60}\n")
        
        # 收集数据
        all_data = self.collect_data(start_date, end_date)
        price_data = all_data['price_data']
        
        # 获取交易日期
        trading_dates = price_data.index.strftime('%Y-%m-%d').tolist()
        
        # 运行每日分析
        daily_results = []
        
        with ProgressTracker(len(trading_dates), "分析进度") as tracker:
            for date in trading_dates:
                try:
                    result = self.run_daily_analysis(date, all_data)
                    daily_results.append(result)
                except Exception as e:
                    print(f"\n⚠️  {date} 分析失败: {str(e)}")
                    # 添加默认结果
                    daily_results.append({
                        'date': date,
                        'symbol': self.symbol,
                        'signal': 0,
                        'final_stance': 'neutral',
                        'final_confidence': 0.5,
                        'consistency': 0.5
                    })
                finally:
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
        
        # 添加我们特有的指标
        metrics['avg_consistency'] = results_df['consistency'].mean()
        metrics['avg_confidence'] = results_df['final_confidence'].mean()
        metrics['avg_confidence_variance'] = results_df.get('confidence_variance', pd.Series([0])).mean()
        metrics['avg_explainability'] = results_df.get('explainability_score', pd.Series([0])).mean()
        
        # 保存结果
        experiment_results = {
            'experiment_name': 'role_based_prompt',
            'symbol': self.symbol,
            'start_date': start_date,
            'end_date': end_date,
            'metrics': metrics,
            'daily_results': results_df.to_dict('records')
        }
        
        print_results_table(metrics, "Role-Based Prompt 实验结果")
        
        save_results(experiment_results, 'role_based_prompt', config.RESULTS_DIR)
        
        return experiment_results


def main():
    """主函数"""
    experiment = RoleBasedPromptExperiment(symbol='AAPL')
    
    results = experiment.run_experiment(
        start_date=config.START_DATE,
        end_date=config.END_DATE
    )
    
    print("\n✅ 实验完成!")


if __name__ == "__main__":
    main()