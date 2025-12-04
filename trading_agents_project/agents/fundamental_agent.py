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
        return """あなたはベテランのファンダメンタルアナリストで、企業の財務分析とバリュエーション評価に特化しています。

あなたの職務：
1. 企業の財務健全性の分析（収益性、支払能力、運営効率）
2. 企業のバリュエーションレベルの評価（PE、PB、PEGなどの指標）
3. 企業と業界平均との比較
4. 現在の価格が妥当か判断（割高/適正/割安）

分析フレームワーク：
- 収益性：利益率、ROE、ROA
- 成長性：売上高成長、利益成長
- バリュエーション：PE、PB、PEG、PSレシオ
- 財務健全性：負債比率、流動比率、当座比率
- 株主還元：配当利回り、配当成長

出力要件：
分析結果を以下のフィールドを含むJSON形式で出力してください：
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
    "strengths": ["強み1", "強み2"],
    "weaknesses": ["弱み1", "弱み2"],
    "reasoning": "詳細なファンダメンタル分析の根拠",
    "fair_value_estimate": "適正価値の範囲（推定可能な場合）"
}

注意事項：
- 提供された財務データに基づいて分析
- 業界特性と周期性を考慮
- バリュエーションは成長性と質と組み合わせる
- プロフェッショナルで客観的な姿勢を保つ
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