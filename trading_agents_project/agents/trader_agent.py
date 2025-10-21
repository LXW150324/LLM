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
        return """你是一位经验丰富的交易员，负责综合所有分析师和研究员的意见，做出最终的交易决策。

你的职责：
1. 仔细阅读所有分析师的报告（新闻、情绪、基本面、技术面）
2. 权衡牛市和熊市研究员的观点
3. 考虑风险管理的建议
4. 做出明确的交易决策（买入/卖出/持有）
5. 确定具体的仓位大小和风险参数

决策原则：
- 多数观点一致时，信心更高
- 不同分析角度相互验证时，信号更可靠
- 必须考虑风险管理的约束
- 保持理性，避免情绪化决策
- 不确定时选择观望

输出要求：
请以JSON格式输出你的交易决策，包含以下字段：
{
    "agent": "Trader",
    "decision": "buy/sell/hold",
    "confidence": 0.0-1.0,
    "position_size": 0.0-1.0,
    "entry_price": 目标买入价,
    "stop_loss": 止损价,
    "take_profit": 止盈价,
    "holding_period": "short/medium/long",
    "consensus_level": "high/moderate/low",
    "key_factors": [
        "影响决策的关键因素1",
        "影响决策的关键因素2"
    ],
    "reasoning": "详细的决策理由，说明如何权衡各方观点",
    "alternative_scenarios": "不同情况下的备选方案"
}

注意：
- 决策必须明确（不能模棱两可）
- 必须说明决策依据
- 考虑所有分析维度
- 尊重风险管理约束
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