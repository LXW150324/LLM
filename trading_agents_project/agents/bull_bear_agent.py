"""
牛熊研究员Agent
分别从看多和看空角度进行辩论和分析
"""

from typing import Dict, List
from .base_agent import BaseAgent

class BullResearcherAgent(BaseAgent):
    """牛市研究员Agent（看多角度）"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Bull Researcher", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取牛市研究员的系统提示词"""
        return """你是一位看多倾向的研究员，专注于发现和强调股票的上涨潜力。

你的职责：
1. 综合分析师团队提供的所有分析报告
2. 从看多（bullish）角度寻找支持买入的理由
3. 强调积极因素和上涨催化剂
4. 对负面因素提出反驳或缓解观点
5. 与熊市研究员进行辩论

分析原则：
- 寻找被低估的价值
- 关注积极的趋势变化
- 强调长期增长潜力
- 但保持理性，不能忽视明显风险

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Bull Researcher",
    "stance": "bullish",
    "confidence": 0.0-1.0,
    "bullish_points": [
        "支持看多的理由1",
        "支持看多的理由2",
        "支持看多的理由3"
    ],
    "catalysts": ["上涨催化剂1", "上涨催化剂2"],
    "risk_mitigation": "对主要风险的缓解看法",
    "reasoning": "详细的看多逻辑",
    "target_upside": "预期上涨空间（百分比或价格）"
}

注意：
- 基于分析师提供的数据和观点
- 保持乐观但理性
- 承认风险但强调机会
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化输入数据"""
        symbol = data.get('symbol', 'Unknown')
        analyst_reports = data.get('analyst_reports', {})
        
        prompt = f"""请从看多（bullish）角度综合分析 {symbol} 股票。

以下是各分析师的报告：

"""
        
        # 添加各个分析师的报告
        for agent_name, report in analyst_reports.items():
            prompt += f"\n【{agent_name}】\n"
            prompt += f"立场: {report.get('stance', 'N/A')}\n"
            prompt += f"分析: {report.get('reasoning', 'N/A')}\n"
            prompt += "-" * 50 + "\n"
        
        prompt += """
请基于以上所有分析师的报告，从看多角度：
1. 找出所有支持买入的理由
2. 识别潜在的上涨催化剂
3. 对负面因素提出缓解观点
4. 给出你的看多信心度

按照指定的JSON格式输出你的分析结果。
"""
        
        return prompt


class BearResearcherAgent(BaseAgent):
    """熊市研究员Agent（看空角度）"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Bear Researcher", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取熊市研究员的系统提示词"""
        return """你是一位看空倾向的研究员，专注于识别股票的下跌风险和负面因素。

你的职责：
1. 综合分析师团队提供的所有分析报告
2. 从看空（bearish）角度寻找支持卖出的理由
3. 强调风险因素和下跌催化剂
4. 对积极因素提出质疑或风险提示
5. 与牛市研究员进行辩论

分析原则：
- 寻找被高估的迹象
- 关注负面趋势和风险
- 强调潜在的下行压力
- 但保持理性，不能过度悲观

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Bear Researcher",
    "stance": "bearish",
    "confidence": 0.0-1.0,
    "bearish_points": [
        "支持看空的理由1",
        "支持看空的理由2",
        "支持看空的理由3"
    ],
    "risk_factors": ["风险因素1", "风险因素2"],
    "optimism_concerns": "对看多观点的质疑",
    "reasoning": "详细的看空逻辑",
    "downside_risk": "预期下跌风险（百分比或价格）"
}

注意：
- 基于分析师提供的数据和观点
- 保持谨慎但理性
- 识别真实风险
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化输入数据"""
        symbol = data.get('symbol', 'Unknown')
        analyst_reports = data.get('analyst_reports', {})
        
        prompt = f"""请从看空（bearish）角度综合分析 {symbol} 股票。

以下是各分析师的报告：

"""
        
        # 添加各个分析师的报告
        for agent_name, report in analyst_reports.items():
            prompt += f"\n【{agent_name}】\n"
            prompt += f"立场: {report.get('stance', 'N/A')}\n"
            prompt += f"分析: {report.get('reasoning', 'N/A')}\n"
            prompt += "-" * 50 + "\n"
        
        prompt += """
请基于以上所有分析师的报告，从看空角度：
1. 找出所有支持卖出的理由
2. 识别潜在的下跌风险因素
3. 对积极因素提出质疑
4. 给出你的看空信心度

按照指定的JSON格式输出你的分析结果。
"""
        
        return prompt