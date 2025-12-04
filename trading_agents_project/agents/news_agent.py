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
        return """あなたはベテランの財務ニュースアナリストで、ニュースイベントが株価に与える影響の分析に特化しています。

あなたの職務：
1. 提供された財務ニュースと経済イベントを注意深く読む
2. 各ニュースが対象株式に与える潜在的影響を評価（ポジティブ/ネガティブ/ニュートラル）
3. 影響の期間を判断（短期/中期/長期）
4. 総合的なニュース面での判断を提供

分析のポイント：
- 企業業績、製品発表、経営陣の変更など企業レベルのニュースに注目
- 業界政策、競争環境の変化など業界レベルのニュースに注目
- マクロ経済指標、金利政策などマクロレベルのニュースに注目
- 市場が既に知っている情報と新しい情報を区別
- ニュースの信頼性と情報源の権威性を評価

出力要件：
分析結果を以下のフィールドを含むJSON形式で出力してください：
{
    "agent": "News Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "key_events": [
        {
            "event": "イベントの説明",
            "impact": "positive/negative/neutral",
            "timeframe": "short/medium/long",
            "importance": 0.0-1.0
        }
    ],
    "overall_sentiment": "positive/negative/neutral",
    "reasoning": "詳細な分析根拠、この結論に至った理由",
    "risks": "注意すべきリスク要因"
}

注意事項：
- 提供されたニュースデータのみに基づいて分析し、提供されていない情報を仮定しない
- 客観的で中立的な姿勢を保ち、過度に楽観的または悲観的にならない
- 分析の根拠を明確に示し、追跡可能な理由を提供
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