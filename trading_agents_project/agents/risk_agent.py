"""
风险管理Agent
专注于风险控制和仓位管理
"""

from typing import Dict
from .base_agent import BaseAgent

class RiskManagementAgent(BaseAgent):
    """风险管理Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Risk Manager", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取风险管理的系统提示词"""
        return """你是一位专业的风险管理专家，负责评估交易风险并提供仓位管理建议。

你的职责：
1. 评估当前交易决策的风险水平
2. 检查是否符合风险控制标准
3. 提供仓位大小建议
4. 设置止损和止盈水平

风险评估维度：
- 市场风险：价格波动、趋势不确定性
- 流动性风险：成交量、买卖价差
- 系统性风险：大盘走势、行业风险
- 特定风险：公司特有风险

输出要求：
请以JSON格式输出你的风险评估结果，包含以下字段：
{
    "agent": "Risk Manager",
    "risk_level": "low/moderate/high/extreme",
    "position_size_recommendation": 0.0-1.0,
    "stop_loss_level": 价格或百分比,
    "take_profit_level": 价格或百分比,
    "max_loss_amount": 最大可承受损失,
    "risk_factors": [
        {
            "factor": "风险因素名称",
            "severity": "low/moderate/high",
            "mitigation": "缓解措施"
        }
    ],
    "approval": true/false,
    "reasoning": "详细的风险评估理由",
    "recommendations": "风险管理建议"
}

风险控制原则：
- 单笔交易风险不超过总资金的2-5%
- 高风险情况下降低仓位
- 必须设置止损
- 考虑整体投资组合风险
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化风险数据"""
        symbol = data.get('symbol', 'Unknown')
        proposed_action = data.get('proposed_action', 'hold')
        current_price = data.get('current_price', 0)
        position_size = data.get('proposed_position_size', 0)
        portfolio_value = data.get('portfolio_value', 100000)
        
        # 获取各分析师的风险提示
        analyst_reports = data.get('analyst_reports', {})
        
        prompt = f"""请评估以下交易决策的风险：

股票: {symbol}
当前价格: ${current_price:.2f}
建议操作: {proposed_action}
建议仓位: {position_size*100:.1f}%
组合总值: ${portfolio_value:,.2f}

各分析师的风险提示:
"""
        
        for agent_name, report in analyst_reports.items():
            if 'risks' in report or 'risk_factors' in report:
                prompt += f"\n【{agent_name}】\n"
                risks = report.get('risks', report.get('risk_factors', []))
                prompt += f"风险提示: {risks}\n"
        
        prompt += """
请基于以上信息：
1. 评估本次交易的整体风险水平
2. 建议合适的仓位大小
3. 设置止损和止盈水平
4. 列出主要风险因素及缓解措施
5. 决定是否批准此交易

按照指定的JSON格式输出你的风险评估结果。
"""
        
        return prompt