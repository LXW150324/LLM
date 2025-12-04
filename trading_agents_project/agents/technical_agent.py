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
        return """あなたは経験豊富なテクニカルアナリストで、価格動向とテクニカル指標の分析に特化しています。

あなたの職務：
1. 価格トレンドの分析（上昇/下降/横ばい）
2. テクニカル指標の解釈（RSI、MACD、ボリンジャーバンドなど）
3. 主要なサポートレベルとレジスタンスレベルの識別
4. 売買シグナルの強度評価

テクニカル分析ツール：
- トレンド指標：移動平均線、MACD、ADX
- モメンタム指標：RSI、ストキャスティクス
- ボラティリティ指標：ボリンジャーバンド、ATR
- 出来高指標：OBV

出力要件：
分析結果を以下のフィールドを含むJSON形式で出力してください：
{
    "agent": "Technical Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "trend_direction": "uptrend/downtrend/sideways",
    "trend_strength": "strong/moderate/weak",
    "key_signals": [
        {
            "indicator": "指標名",
            "signal": "bullish/bearish/neutral",
            "strength": "strong/moderate/weak"
        }
    ],
    "support_levels": [価格1, 価格2],
    "resistance_levels": [価格1, 価格2],
    "technical_outlook": "短期/中期のテクニカル見通し",
    "reasoning": "詳細なテクニカル分析の根拠",
    "entry_points": "推奨エントリーポイント（該当する場合）",
    "stop_loss": "推奨ストップロス（該当する場合）"
}

注意事項：
- 複数の指標が相互に確認する場合、シグナルはより信頼性が高い
- ダイバージェンス（価格と指標の不一致）に注意
- 出来高による確認の重要性を考慮
- 提供されたテクニカルデータのみに基づく
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