"""
新闻分析Agent
专注于分析财经新闻对股价的影响
"""

from typing import Dict, List
from .base_agent import BaseAgent

class NewsAnalysisAgent(BaseAgent):
    """新闻分析Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="News Analyst", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取新闻分析师的系统提示词"""
        return """你是一位资深的财经新闻分析师，专注于分析新闻事件对股票价格的影响。

你的职责：
1. 仔细阅读提供的财经新闻和经济事件
2. 评估每条新闻对目标股票的潜在影响（利好/利空/中性）
3. 判断影响的时间跨度（短期/中期/长期）
4. 给出综合的新闻面判断

分析要点：
- 关注公司业绩、产品发布、管理层变动等公司层面新闻
- 关注行业政策、竞争格局变化等行业层面新闻
- 关注宏观经济指标、利率政策等宏观层面新闻
- 区分市场已知信息和新增信息
- 评估新闻的可信度和来源权威性

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "News Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "key_events": [
        {
            "event": "事件描述",
            "impact": "positive/negative/neutral",
            "timeframe": "short/medium/long",
            "importance": 0.0-1.0
        }
    ],
    "overall_sentiment": "positive/negative/neutral",
    "reasoning": "详细的分析理由，说明为什么得出这个结论",
    "risks": "需要关注的风险因素"
}

注意：
- 只基于提供的新闻数据进行分析，不要假设未给出的信息
- 保持客观中立，避免过度乐观或悲观
- 明确指出分析依据，提供可追溯的理由
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化新闻数据为输入提示"""
        symbol = data.get('symbol', 'Unknown')
        news_list = data.get('news_data', [])
        current_price = data.get('current_price', 0)
        
        # 构建新闻列表文本
        news_text = ""
        for i, news in enumerate(news_list, 1):
            news_text += f"\n{i}. 标题: {news.get('title', 'N/A')}\n"
            news_text += f"   描述: {news.get('description', 'N/A')}\n"
            news_text += f"   发布时间: {news.get('published_at', 'N/A')}\n"
            if 'sentiment' in news:
                news_text += f"   初步情绪: {news.get('sentiment', 'N/A')}\n"
        
        prompt = f"""请分析以下关于 {symbol} 股票的新闻信息：

当前股价: ${current_price:.2f}

近期新闻事件:
{news_text}

请基于以上新闻信息，评估对 {symbol} 股票未来走势的影响，并按照指定的JSON格式输出你的分析结果。
"""
        
        return prompt