"""
技术分析Agent
专注于价格走势和技术指标分析
"""

from typing import Dict
from .base_agent import BaseAgent

class TechnicalAnalysisAgent(BaseAgent):
    """技术分析Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(role_name="Technical Analyst", api_key=api_key)
    
    def get_system_prompt(self) -> str:
        """获取技术分析师的系统提示词"""
        return """你是一位经验丰富的技术分析师，专注于价格走势和技术指标分析。

你的职责：
1. 分析价格趋势（上升/下降/横盘）
2. 解读技术指标（RSI、MACD、布林带等）
3. 识别关键支撑位和阻力位
4. 评估买卖信号的强度

技术分析工具：
- 趋势指标：移动平均线、MACD、ADX
- 动量指标：RSI、随机指标
- 波动率指标：布林带、ATR
- 成交量指标：OBV

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Technical Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "trend_direction": "uptrend/downtrend/sideways",
    "trend_strength": "strong/moderate/weak",
    "key_signals": [
        {
            "indicator": "指标名称",
            "signal": "bullish/bearish/neutral",
            "strength": "strong/moderate/weak"
        }
    ],
    "support_levels": [价格1, 价格2],
    "resistance_levels": [价格1, 价格2],
    "technical_outlook": "短期/中期技术面展望",
    "reasoning": "详细的技术分析理由",
    "entry_points": "建议的进场点位（如果有）",
    "stop_loss": "建议的止损位（如果有）"
}

注意：
- 多个指标相互验证时信号更可靠
- 注意背离现象（价格与指标的不一致）
- 考虑成交量的确认作用
- 只基于提供的技术数据
"""
    
    def format_input_data(self, data: Dict) -> str:
        """格式化技术数据为输入提示"""
        symbol = data.get('symbol', 'Unknown')
        tech_summary = data.get('technical_summary', {})
        
        price_info = tech_summary.get('price', {})
        trend_info = tech_summary.get('trend', {})
        momentum_info = tech_summary.get('momentum', {})
        volatility_info = tech_summary.get('volatility', {})
        volume_info = tech_summary.get('volume', {})
        strength_info = tech_summary.get('strength', {})
        
        prompt = f"""请分析以下 {symbol} 股票的技术面数据：

价格信息:
- 当前价: ${price_info.get('current', 0):.2f}
- 开盘价: ${price_info.get('open', 0):.2f}
- 最高价: ${price_info.get('high', 0):.2f}
- 最低价: ${price_info.get('low', 0):.2f}
- 涨跌幅: {price_info.get('change_pct', 0):+.2f}%
- 成交量: {price_info.get('volume', 0):,}

趋势指标:
- 20日均线: ${trend_info.get('sma_short', 0):.2f}
- 50日均线: ${trend_info.get('sma_long', 0):.2f}
- EMA12: ${trend_info.get('ema_12', 0):.2f}
- EMA26: ${trend_info.get('ema_26', 0):.2f}
- 趋势方向: {trend_info.get('trend_direction', 'N/A')}

动量指标:
- RSI(14): {momentum_info.get('rsi', 0):.2f} ({momentum_info.get('rsi_signal', 'N/A')})
- MACD: {momentum_info.get('macd', 0):.4f}
- MACD信号线: {momentum_info.get('macd_signal', 0):.4f}
- MACD柱状图: {momentum_info.get('macd_histogram', 0):.4f}
- 随机指标K: {momentum_info.get('stoch_k', 0):.2f}
- 随机指标D: {momentum_info.get('stoch_d', 0):.2f}

波动率指标:
- 布林带上轨: ${volatility_info.get('bb_upper', 0):.2f}
- 布林带中轨: ${volatility_info.get('bb_middle', 0):.2f}
- 布林带下轨: ${volatility_info.get('bb_lower', 0):.2f}
- 布林带宽度: {volatility_info.get('bb_width', 0):.4f}
- 价格位置: {volatility_info.get('position', 'N/A')}
- ATR: {volatility_info.get('atr', 0):.2f}

成交量指标:
- OBV: {volume_info.get('obv', 0):,.0f}
- 成交量变化: {volume_info.get('volume_change_pct', 0):+.2f}%

趋势强度:
- ADX: {strength_info.get('adx', 0):.2f}
- 趋势强度: {strength_info.get('trend_strength', 'N/A')}

请基于以上技术指标，评估 {symbol} 的技术面，并按照指定的JSON格式输出你的分析结果。

分析时请考虑：
1. 多个指标是否相互确认？
2. 是否存在超买/超卖情况？
3. 是否存在背离现象？
4. 成交量是否支持当前走势？
"""
        
        return prompt