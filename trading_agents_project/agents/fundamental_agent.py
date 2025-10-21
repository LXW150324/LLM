"""
基本面分析Agent
专注于公司财务和估值分析
"""

from typing import Dict
from .base_agent import BaseAgent

class FundamentalAnalysisAgent(BaseAgent):
    """基本面分析Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Fundamental Analyst", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取基本面分析师的系统提示词"""
        return """你是一位资深的基本面分析师，专注于公司财务分析和估值评估。

你的职责：
1. 分析公司的财务健康状况（盈利能力、偿债能力、运营效率）
2. 评估公司估值水平（PE、PB、PEG等指标）
3. 比较公司与行业平均水平
4. 判断当前价格是否合理（高估/低估/合理）

分析框架：
- 盈利能力：利润率、ROE、ROA
- 成长性：营收增长、利润增长
- 估值水平：PE、PB、PEG、PS比率
- 财务健康：负债率、流动比率、速动比率
- 股东回报：股息率、股息增长

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Fundamental Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "valuation_assessment": "undervalued/fairly_valued/overvalued",
    "financial_health": "excellent/good/fair/poor",
    "growth_outlook": "strong/moderate/weak",
    "key_metrics": {
        "pe_ratio": 0.0,
        "pb_ratio": 0.0,
        "roe": 0.0,
        "debt_to_equity": 0.0,
        "profit_margin": 0.0
    },
    "strengths": ["优势1", "优势2"],
    "weaknesses": ["劣势1", "劣势2"],
    "reasoning": "详细的基本面分析理由",
    "fair_value_estimate": "合理估值范围（如果可以估算）"
}

注意：
- 基于提供的财务数据进行分析
- 考虑行业特性和周期性
- 估值应结合成长性和质量
- 保持专业和客观
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化财务数据为输入提示"""
        symbol = data.get('symbol', 'Unknown')
        financial_data = data.get('financial_data', {})
        current_price = data.get('current_price', 0)
        
        prompt = f"""请分析以下 {symbol} 股票的基本面数据：

当前股价: ${current_price:.2f}

公司基本信息:
- 行业: {financial_data.get('sector', 'N/A')}
- 细分行业: {financial_data.get('industry', 'N/A')}
- 市值: ${financial_data.get('market_cap', 0):,.0f}

估值指标:
- 市盈率(PE): {financial_data.get('pe_ratio', 0):.2f}
- 远期市盈率: {financial_data.get('forward_pe', 0):.2f}
- 市净率(PB): {financial_data.get('price_to_book', 0):.2f}
- PEG比率: {financial_data.get('peg_ratio', 0):.2f}

盈利能力:
- 净利润率: {financial_data.get('profit_margin', 0)*100:.2f}%
- 营业利润率: {financial_data.get('operating_margin', 0)*100:.2f}%
- 净资产收益率(ROE): {financial_data.get('roe', 0)*100:.2f}%

成长性:
- 营收增长率: {financial_data.get('revenue_growth', 0)*100:.2f}%
- 利润增长率: {financial_data.get('earnings_growth', 0)*100:.2f}%

财务健康:
- 负债权益比: {financial_data.get('debt_to_equity', 0):.2f}
- 流动比率: {financial_data.get('current_ratio', 0):.2f}
- 速动比率: {financial_data.get('quick_ratio', 0):.2f}

其他指标:
- 股息率: {financial_data.get('dividend_yield', 0)*100:.2f}%
- Beta系数: {financial_data.get('beta', 1.0):.2f}

请基于以上财务数据，评估 {symbol} 的投资价值，并按照指定的JSON格式输出你的分析结果。
"""
        
        return prompt