"""
交易决策Agent
综合所有分析做出最终交易决策
"""

from typing import Dict, List
from .base_agent import BaseAgent

class TraderAgent(BaseAgent):
    """交易决策Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Trader", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取交易员的系统提示词"""
        return """あなたは経験豊富なトレーダーで、すべてのアナリストと研究者の意見を統合し、最終的な取引決定を行う責任があります。

あなたの職務：
1. すべてのアナリストのレポートを注意深く読む（ニュース、センチメント、ファンダメンタル、テクニカル）
2. 強気と弱気の研究者の見解を比較検討
3. リスク管理の提案を考慮
4. 明確な取引決定を行う（買い/売り/保有）
5. 具体的なポジションサイズとリスクパラメータを決定

意思決定の原則：
- 多数意見が一致する場合、信頼度が高い
- 異なる分析角度が相互に確認する場合、シグナルはより信頼性が高い
- リスク管理の制約を必ず考慮
- 理性を保ち、感情的な決定を避ける
- 不確実な場合は様子見を選択

出力要件：
取引決定を以下のフィールドを含むJSON形式で出力してください：
{
    "agent": "Trader",
    "decision": "buy/sell/hold",
    "confidence": 0.0-1.0,
    "position_size": 0.0-1.0,
    "entry_price": 目標購入価格,
    "stop_loss": ストップロス価格,
    "take_profit": 利益確定価格,
    "holding_period": "short/medium/long",
    "consensus_level": "high/moderate/low",
    "key_factors": [
        "決定に影響する重要要因1",
        "決定に影響する重要要因2"
    ],
    "reasoning": "詳細な決定根拠、各意見をどのように比較検討したか",
    "alternative_scenarios": "異なる状況下での代替案"
}

注意事項：
- 決定は明確でなければならない（曖昧であってはならない）
- 決定の根拠を必ず説明
- すべての分析次元を考慮
- リスク管理の制約を尊重
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化交易决策输入"""
        symbol = data.get('symbol', 'Unknown')
        current_price = data.get('current_price', 0)
        
        # 获取所有分析报告
        fundamental_report = data.get('fundamental_analysis', {})
        technical_report = data.get('technical_analysis', {})
        sentiment_report = data.get('sentiment_analysis', {})
        news_report = data.get('news_analysis', {})
        bull_report = data.get('bull_research', {})
        bear_report = data.get('bear_research', {})
        risk_report = data.get('risk_assessment', {})
        
        prompt = f"""请为 {symbol} 股票做出交易决策。

当前价格: ${current_price:.2f}

【基本面分析】
立场: {fundamental_report.get('stance', 'N/A')}
信心度: {fundamental_report.get('confidence', 0):.2f}
关键观点: {fundamental_report.get('reasoning', 'N/A')[:200]}

【技术面分析】
立场: {technical_report.get('stance', 'N/A')}
信心度: {technical_report.get('confidence', 0):.2f}
关键观点: {technical_report.get('reasoning', 'N/A')[:200]}

【情绪分析】
立场: {sentiment_report.get('stance', 'N/A')}
信心度: {sentiment_report.get('confidence', 0):.2f}
关键观点: {sentiment_report.get('reasoning', 'N/A')[:200]}

【新闻分析】
立场: {news_report.get('stance', 'N/A')}
信心度: {news_report.get('confidence', 0):.2f}
关键观点: {news_report.get('reasoning', 'N/A')[:200]}

【牛市研究员观点】
信心度: {bull_report.get('confidence', 0):.2f}
看多理由: {bull_report.get('bullish_points', [])}

【熊市研究员观点】
信心度: {bear_report.get('confidence', 0):.2f}
看空理由: {bear_report.get('bearish_points', [])}

【风险管理建议】
风险级别: {risk_report.get('risk_level', 'N/A')}
建议仓位: {risk_report.get('position_size_recommendation', 0)*100:.1f}%
止损建议: {risk_report.get('stop_loss_level', 'N/A')}
是否批准: {risk_report.get('approval', True)}

请基于以上所有信息：
1. 做出明确的交易决策（buy/sell/hold）
2. 确定仓位大小
3. 设置止损和止盈
4. 说明决策理由（如何权衡各方观点）
5. 评估团队意见的一致性水平

按照指定的JSON格式输出你的交易决策。
"""
        
        return prompt