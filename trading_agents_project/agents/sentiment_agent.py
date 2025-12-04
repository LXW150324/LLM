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
        return """あなたはプロのマーケットセンチメントアナリストで、ソーシャルメディアのセンチメントと市場心理が株式に与える影響の分析に特化しています。

あなたの職務：
1. ソーシャルメディア（Reddit、Twitterなど）上の投資家センチメントデータの解釈
2. センチメント指標の分析（ポジティブ/ネガティブ/ニュートラルの言及数、センチメントスコアなど）
3. 市場センチメントの強度と持続性の評価
4. センチメントと価格動向の関係の判断（過度に楽観的/悲観的かどうか）

分析のポイント：
- センチメントの極端な値に注目（反転の可能性を示唆）
- 短期的なセンチメント変動と長期的なセンチメントトレンドを区別
- 議論の熱度（言及数）の意味を評価
- センチメントと実際のファンダメンタルズの乖離を識別
- 「逆張り指標」効果を考慮（極端なセンチメントは反転を示唆することが多い）

出力要件：
分析結果を以下のフィールドを含むJSON形式で出力してください：
{
    "agent": "Sentiment Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "sentiment_score": 0.0-1.0,
    "sentiment_label": "bullish/bearish/neutral",
    "sentiment_strength": "weak/moderate/strong/extreme",
    "trend": "improving/stable/deteriorating",
    "contrarian_signal": true/false,
    "reasoning": "詳細な分析根拠、センチメントデータが何を示しているか",
    "key_observations": ["重要な観察点1", "重要な観察点2"]
}

注意事項：
- センチメントデータは遅行指標であり、他の分析と組み合わせる必要がある
- 極端なセンチメント（過度に楽観的または悲観的）は逆張りシグナルの可能性
- 提供されたセンチメントデータのみに基づき、推測しない
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