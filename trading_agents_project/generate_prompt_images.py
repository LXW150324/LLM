#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Agent提示词的PNG图片
为每个Agent的提示词创建一张精美的图片
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import os

# Agent提示词数据
AGENTS = [
    {
        "name": "Agent 1: 技术分析师 (Technical Analyst)",
        "subtitle": "负责价格走势和技术指标分析",
        "file": "agents/technical_agent.py",
        "lines": "第15-59行",
        "fields": "11个",
        "prompt": """你是一位经验丰富的技术分析师，专注于价格走势和技术指标分析。

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
- 只基于提供的技术数据"""
    },
    {
        "name": "Agent 2: 基本面分析师 (Fundamental Analyst)",
        "subtitle": "负责公司财务和估值分析",
        "file": "agents/fundamental_agent.py",
        "lines": "第15-59行",
        "fields": "10个",
        "prompt": """你是一位资深的基本面分析师，专注于公司财务分析和估值评估。

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
- 保持专业和客观"""
    },
    {
        "name": "Agent 3: 情绪分析师 (Sentiment Analyst)",
        "subtitle": "负责市场情绪和社交媒体分析",
        "file": "agents/sentiment_agent.py",
        "lines": "第15-51行",
        "fields": "10个",
        "prompt": """你是一位专业的市场情绪分析师，专注于分析社交媒体情绪和市场心理对股票的影响。

你的职责：
1. 解读社交媒体（如Reddit、Twitter）上的投资者情绪数据
2. 分析情绪指标（正面/负面/中性提及次数、情绪得分等）
3. 评估市场情绪的强度和可持续性
4. 判断情绪与价格走势的关系（是否过度乐观/悲观）

分析要点：
- 关注情绪的极端值（可能预示反转）
- 区分短期情绪波动和长期情绪趋势
- 评估讨论热度（提及次数）的意义
- 识别情绪与实际基本面的背离
- 考虑"逆向指标"效应（极端情绪往往预示反转）

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "Sentiment Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "sentiment_score": 0.0-1.0,
    "sentiment_label": "bullish/bearish/neutral",
    "sentiment_strength": "weak/moderate/strong/extreme",
    "trend": "improving/stable/deteriorating",
    "contrarian_signal": true/false,
    "reasoning": "详细的分析理由，说明情绪数据透露了什么信息",
    "key_observations": ["关键观察点1", "关键观察点2"]
}

注意：
- 情绪数据是滞后指标，需要结合其他分析
- 极端情绪（过度乐观或悲观）可能是反向信号
- 只基于提供的情绪数据，不要臆测"""
    },
    {
        "name": "Agent 4: 新闻分析师 (News Analyst)",
        "subtitle": "负责新闻事件影响分析",
        "file": "agents/news_agent.py",
        "lines": "第15-55行",
        "fields": "7个",
        "prompt": """你是一位资深的财经新闻分析师，专注于分析新闻事件对股票价格的影响。

你的职责：
1. 仔细阅读提供的财经新闻和经济事件
2. 评估每条新闻对目标股票的潜在影响（利好/利空/中性）
3. 判断影响的时间跨度（短期/中期/长期）
4. 给出综合的新闻面判断

分析要点：
- 关注公司业绩、产品发布、管理层变动等公司层面新闻
- 关注行业政策、竞争格局变化等行业层面新闻
- 关注宏观经济指标、利率政策等宏观层面新闻
- 区分市场已知信息和新增信息
- 评估新闻的可信度和来源权威性

输出要求：
请以JSON格式输出你的分析结果，包含以下字段：
{
    "agent": "News Analyst",
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "key_events": [
        {
            "event": "事件描述",
            "impact": "positive/negative/neutral",
            "timeframe": "short/medium/long",
            "importance": 0.0-1.0
        }
    ],
    "overall_sentiment": "positive/negative/neutral",
    "reasoning": "详细的分析理由，说明为什么得出这个结论",
    "risks": "需要关注的风险因素"
}

注意：
- 只基于提供的新闻数据进行分析，不要假设未给出的信息
- 保持客观中立，避免过度乐观或悲观
- 明确指出分析依据，提供可追溯的理由"""
    },
    {
        "name": "Agent 5: 交易决策者 (Trader)",
        "subtitle": "负责综合决策和风险管理",
        "file": "agents/trader_agent.py",
        "lines": "第15-58行",
        "fields": "12个",
        "prompt": """你是一位经验丰富的交易员，负责综合所有分析师和研究员的意见，做出最终的交易决策。

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
- 尊重风险管理约束"""
    }
]


def create_gradient_background(width, height, color1, color2):
    """创建渐变背景"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def create_prompt_image(agent_data, output_path):
    """为单个Agent创建图片"""

    # 图片尺寸
    width = 1200
    margin = 60
    content_width = width - 2 * margin

    # 颜色定义
    bg_color1 = (102, 126, 234)  # #667eea
    bg_color2 = (118, 75, 162)   # #764ba2
    white = (255, 255, 255)
    light_gray = (240, 240, 240)
    dark_gray = (60, 60, 60)

    # 使用支持中文的字体
    try:
        # 优先使用文泉驿正黑字体（支持中文）
        chinese_font = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
        title_font = ImageFont.truetype(chinese_font, 28)
        subtitle_font = ImageFont.truetype(chinese_font, 16)
        text_font = ImageFont.truetype(chinese_font, 13)
        meta_font = ImageFont.truetype(chinese_font, 13)
    except Exception as e:
        print(f"⚠ 警告: 无法加载中文字体: {e}")
        # 如果找不到字体，使用默认字体
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        meta_font = ImageFont.load_default()

    # 准备文本内容
    lines = agent_data['prompt'].split('\n')
    wrapped_lines = []
    for line in lines:
        if len(line) <= 80:
            wrapped_lines.append(line)
        else:
            # 手动换行长行
            wrapped_lines.extend(textwrap.wrap(line, width=80))

    # 计算需要的高度
    header_height = 140
    line_height = 20
    content_height = len(wrapped_lines) * line_height + 40
    meta_height = 80
    total_height = header_height + content_height + meta_height + 60

    # 创建渐变背景
    img = create_gradient_background(width, total_height, bg_color1, bg_color2)
    draw = ImageDraw.Draw(img)

    # 绘制标题卡片（白色背景）
    card_y = margin
    card_height = total_height - 2 * margin
    draw.rounded_rectangle(
        [(margin, card_y), (width - margin, card_y + card_height)],
        radius=12,
        fill=white
    )

    # 绘制标题区域（渐变背景）
    header_y = card_y
    header_gradient = create_gradient_background(
        width - 2 * margin, header_height, bg_color1, bg_color2
    )
    img.paste(header_gradient, (margin, header_y))

    # 绘制标题文字
    title_y = header_y + 30
    draw.text((margin + 30, title_y), agent_data['name'], fill=white, font=title_font)
    subtitle_y = title_y + 45
    draw.text((margin + 30, subtitle_y), agent_data['subtitle'], fill=white, font=subtitle_font)

    # 绘制提示词内容
    content_y = header_y + header_height + 30
    current_y = content_y

    for line in wrapped_lines:
        draw.text((margin + 30, current_y), line, fill=dark_gray, font=text_font)
        current_y += line_height

    # 绘制元数据区域（浅灰色背景）
    meta_y = current_y + 20
    draw.rounded_rectangle(
        [(margin + 20, meta_y), (width - margin - 20, meta_y + meta_height)],
        radius=8,
        fill=light_gray
    )

    # 绘制元数据文字
    meta_text_y = meta_y + 20
    draw.text((margin + 40, meta_text_y), f"代码文件: {agent_data['file']}", fill=dark_gray, font=meta_font)
    draw.text((margin + 40, meta_text_y + 25), f"行数: {agent_data['lines']}", fill=dark_gray, font=meta_font)
    draw.text((margin + 40, meta_text_y + 50), f"字段数: {agent_data['fields']}", fill=dark_gray, font=meta_font)

    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("开始生成Agent提示词图片...\n")

    # 创建输出目录
    output_dir = "prompt_images"
    os.makedirs(output_dir, exist_ok=True)

    # 为每个Agent生成图片
    for i, agent in enumerate(AGENTS, 1):
        output_path = os.path.join(output_dir, f"agent_{i}_prompt.png")
        create_prompt_image(agent, output_path)

    print(f"\n✅ 完成！所有图片已保存到 {output_dir}/ 目录")
    print(f"   共生成 {len(AGENTS)} 张图片")


if __name__ == "__main__":
    main()
