"""
情绪分析Agent
专注于分析社交媒体和市场情绪
"""

from typing import Dict
from .base_agent import BaseAgent

class SentimentAnalysisAgent(BaseAgent):
    """情绪分析Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Sentiment Analyst", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取情绪分析师的系统提示词"""
        return """你是一位专业的市场情绪分析师，专注于分析社交媒体情绪和市场心理对股票的影响。

你的职责：
1. 解读社交媒体（如Reddit、Twitter）上的投资者情绪数据
2. 分析情绪指标（正面/负面/中性提及次数、情绪得分等）
3. 评估市场情绪的强度和可持续性
4. 判断情绪与价格走势的关系（是否过度乐观/悲观）

分析要点：
- 关注情绪的极端值（可能预示反转）
- 区分短期情绪波动和长期情绪趋势
- 评估讨论热度（提及次数）的意义
- 识别情绪与实际基本面的背离
- 考虑"逆向指标"效应（极端情绪往往预示反转）

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Sentiment Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "sentiment_score": 0.0-1.0,
    "sentiment_label": "bullish/bearish/neutral",
    "sentiment_strength": "weak/moderate/strong/extreme",
    "trend": "improving/stable/deteriorating",
    "contrarian_signal": true/false,
    "reasoning": "详细的分析理由，说明情绪数据透露了什么信息",
    "key_observations": ["关键观察点1", "关键观察点2"]
}

注意：
- 情绪数据是滞后指标，需要结合其他分析
- 极端情绪（过度乐观或悲观）可能是反向信号
- 只基于提供的情绪数据，不要臆测
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化情绪数据为输入提示"""
        symbol = data.get('symbol', 'Unknown')
        sentiment_data = data.get('sentiment_data', {})
        current_price = data.get('current_price', 0)
        price_change = data.get('price_change', 0)
        
        prompt = f"""请分析以下关于 {symbol} 股票的社交媒体情绪数据：

当前股价: ${current_price:.2f}
今日涨跌幅: {price_change:+.2f}%

社交媒体情绪数据:
- 情绪得分: {sentiment_data.get('sentiment_score', 0):.2f} (0=极度悲观, 1=极度乐观)
- 情绪标签: {sentiment_data.get('sentiment_label', 'N/A')}
- 正面提及: {sentiment_data.get('positive_mentions', 0)} 次
- 负面提及: {sentiment_data.get('negative_mentions', 0)} 次
- 中性提及: {sentiment_data.get('neutral_mentions', 0)} 次
- 总讨论量: {sentiment_data.get('total_mentions', 0)} 次
- 热度趋势: {sentiment_data.get('trending_score', 0):.2f}

请基于以上情绪数据，评估市场情绪对 {symbol} 股票的影响，并按照指定的JSON格式输出你的分析结果。

特别注意：
1. 当前情绪是否过于极端？
2. 情绪与价格走势是否一致？
3. 是否存在逆向投资机会？
"""
        
        return prompt