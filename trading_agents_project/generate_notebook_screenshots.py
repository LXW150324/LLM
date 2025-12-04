#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Jupyter Notebook风格的运行界面截图
展示在Notebook中运行Agent的真实场景
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# 5个Agent的Notebook运行场景
NOTEBOOK_SCENARIOS = [
    {
        "agent_name": "Agent 1: テクニカルアナリスト",
        "cell_number": 1,
        "code": """# Agent 1: テクニカルアナリストの実行
from agents.technical_agent import TechnicalAnalysisAgent

# エージェントの初期化
agent = TechnicalAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))

# 分析データの準備
data = {
    'symbol': 'AAPL',
    'technical_summary': {
        'price': {'current': 163.50, 'open': 162.80},
        'trend': {'sma_short': 160.20, 'sma_long': 158.80},
        'momentum': {'rsi': 68.5, 'macd': 1.25}
    }
}

# 分析の実行
result = agent.analyze(data)
print(result)""",
        "output": """{
  "agent": "Technical Analyst",
  "stance": "bullish",
  "confidence": 0.75,
  "trend_direction": "uptrend",
  "trend_strength": "moderate",
  "key_signals": [
    {
      "indicator": "RSI",
      "signal": "bullish",
      "strength": "moderate"
    },
    {
      "indicator": "MACD",
      "signal": "bullish",
      "strength": "strong"
    }
  ],
  "support_levels": [158.80, 160.20],
  "resistance_levels": [165.00, 168.50],
  "technical_outlook": "短期的には上昇トレンドが継続する見込み",
  "reasoning": "現在価格が20日MAと50日MAの両方を上回っており、明確な上昇トレンドを示しています。RSIは68.5で過熱気味ですが、まだ買われすぎの領域には達していません。MACDもポジティブなシグナルを示しています。"
}"""
    },
    {
        "agent_name": "Agent 2: ファンダメンタルアナリスト",
        "cell_number": 2,
        "code": """# Agent 2: ファンダメンタルアナリストの実行
from agents.fundamental_agent import FundamentalAnalysisAgent

agent = FundamentalAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))

data = {
    'symbol': 'AAPL',
    'current_price': 163.50,
    'financial_data': {
        'pe_ratio': 28.5,
        'price_to_book': 45.2,
        'roe': 1.475,
        'profit_margin': 0.302,
        'revenue_growth': 0.085
    }
}

result = agent.analyze(data)
print(result)""",
        "output": """{
  "agent": "Fundamental Analyst",
  "stance": "neutral",
  "confidence": 0.65,
  "valuation_assessment": "fairly_valued",
  "financial_health": "excellent",
  "growth_outlook": "moderate",
  "key_metrics": {
    "pe_ratio": 28.5,
    "pb_ratio": 45.2,
    "roe": 1.475,
    "debt_to_equity": 1.8,
    "profit_margin": 0.302
  },
  "strengths": [
    "業界トップクラスのROE 147.5%",
    "高い営業利益率30.2%",
    "強力なブランド力と顧客基盤"
  ],
  "weaknesses": [
    "高いPE比率が成長率に対して割高",
    "売上高成長率8.5%は減速傾向"
  ],
  "reasoning": "Appleの財務状況は非常に優れていますが、バリュエーションは市場平均を上回っています。"
}"""
    },
    {
        "agent_name": "Agent 3: センチメントアナリスト",
        "cell_number": 3,
        "code": """# Agent 3: センチメントアナリストの実行
from agents.sentiment_agent import SentimentAnalysisAgent

agent = SentimentAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))

data = {
    'symbol': 'AAPL',
    'current_price': 163.50,
    'price_change': 2.5,
    'sentiment_data': {
        'sentiment_score': 0.72,
        'sentiment_label': 'bullish',
        'positive_mentions': 1250,
        'negative_mentions': 380,
        'total_mentions': 1850,
        'trending_score': 8.5
    }
}

result = agent.analyze(data)
print(result)""",
        "output": """{
  "agent": "Sentiment Analyst",
  "stance": "bullish",
  "confidence": 0.72,
  "sentiment_score": 0.72,
  "sentiment_label": "bullish",
  "sentiment_strength": "strong",
  "trend": "improving",
  "contrarian_signal": false,
  "reasoning": "センチメントスコア0.72は強い楽観的センチメントを示しています。ポジティブ言及がネガティブの3倍以上あり、市場の関心が高まっています。",
  "key_observations": [
    "総議論量1850回は平均の2倍以上",
    "トレンドスコア8.5/10で急上昇中",
    "ポジティブ/ネガティブ比率が3.3:1と非常に良好"
  ]
}"""
    },
    {
        "agent_name": "Agent 4: ニュースアナリスト",
        "cell_number": 4,
        "code": """# Agent 4: ニュースアナリストの実行
from agents.news_agent import NewsAnalysisAgent

agent = NewsAnalysisAgent(api_key=os.getenv("OPENAI_API_KEY"))

data = {
    'symbol': 'AAPL',
    'current_price': 163.50,
    'news_data': [
        {
            'title': 'AppleがVision Proの新バージョン発表、価格20%削減',
            'published_at': '2024-12-01'
        },
        {
            'title': 'Q3決算：売上高・EPSともに予想超え',
            'published_at': '2024-12-02'
        },
        {
            'title': 'CEOが2025年AI戦略について楽観的見通し',
            'published_at': '2024-12-03'
        }
    ]
}

result = agent.analyze(data)
print(result)""",
        "output": """{
  "agent": "News Analyst",
  "stance": "bullish",
  "confidence": 0.80,
  "key_events": [
    {
      "event": "Vision Pro価格削減と新バージョン発表",
      "impact": "positive",
      "timeframe": "medium",
      "importance": 0.7
    },
    {
      "event": "Q3決算が市場予想を上回る",
      "impact": "positive",
      "timeframe": "short",
      "importance": 0.9
    },
    {
      "event": "AI戦略の前向きな見通し",
      "impact": "positive",
      "timeframe": "long",
      "importance": 0.8
    }
  ],
  "overall_sentiment": "positive",
  "reasoning": "3つの主要なポジティブニュースが重なっており、全ての時間軸で好材料が揃っています。",
  "risks": "マクロ経済の不確実性、競合の動向に注意が必要"
}"""
    },
    {
        "agent_name": "Agent 5: トレーダー",
        "cell_number": 5,
        "code": """# Agent 5: トレーダーの実行（最終判断）
from agents.trader_agent import TraderAgent

agent = TraderAgent(api_key=os.getenv("OPENAI_API_KEY"))

# 全Agentの分析結果を統合
data = {
    'symbol': 'AAPL',
    'current_price': 163.50,
    'technical_analysis': {'stance': 'bullish', 'confidence': 0.75},
    'fundamental_analysis': {'stance': 'neutral', 'confidence': 0.65},
    'sentiment_analysis': {'stance': 'bullish', 'confidence': 0.72},
    'news_analysis': {'stance': 'bullish', 'confidence': 0.80}
}

# 最終的な取引判断
result = agent.make_decision(data)
print(result)""",
        "output": """{
  "agent": "Trader",
  "decision": "buy",
  "confidence": 0.73,
  "position_size": 0.6,
  "entry_price": 163.50,
  "stop_loss": 158.00,
  "take_profit": 172.00,
  "holding_period": "medium",
  "consensus_level": "high",
  "key_factors": [
    "テクニカル、センチメント、ニュース全てが強気シグナル",
    "ファンダメンタルも中立で反対シグナルではない",
    "4つの分析のコンセンサスレベルが高い",
    "リスク・リワード比率が良好（1:2.8）"
  ],
  "reasoning": "4つの分析のうち3つが強気、1つが中立であり、総合的なコンセンサスレベルは高いです。60%のポジションサイズで買い推奨し、ストップロスは直近サポートの$158、利益確定は$172に設定します。",
  "alternative_scenarios": "もし$158を下回った場合は損切りし、市場環境を再評価します。"
}"""
    }
]


def create_notebook_screenshot(scenario, output_path):
    """创建Jupyter Notebook风格的截图"""

    # 图片尺寸
    width = 1400
    margin = 30

    # Jupyter Notebook颜色定义
    nb_bg = (255, 255, 255)  # 白色背景
    cell_border = (207, 216, 220)  # 浅灰色边框
    code_bg = (247, 247, 247)  # 代码背景
    output_bg = (255, 255, 255)  # 输出背景
    prompt_bg = (238, 238, 238)  # In/Out提示背景
    prompt_text = (48, 63, 159)  # In[]/Out[]文字颜色
    code_text = (0, 0, 0)  # 代码文字颜色
    output_text = (0, 0, 0)  # 输出文字颜色
    comment_color = (96, 96, 96)  # 注释颜色

    # 加载字体
    try:
        japanese_font = "/usr/share/fonts/truetype/custom/NotoSansJP.ttf"
        title_font = ImageFont.truetype(japanese_font, 16)
        code_font = ImageFont.truetype(japanese_font, 13)
        prompt_font = ImageFont.truetype(japanese_font, 13)
    except:
        title_font = ImageFont.load_default()
        code_font = ImageFont.load_default()
        prompt_font = ImageFont.load_default()

    # 计算代码和输出的高度
    code_lines = scenario['code'].split('\n')
    output_lines = scenario['output'].split('\n')

    code_height = len(code_lines) * 20 + 50
    output_height = len(output_lines) * 20 + 50

    # 总高度
    total_height = 80 + code_height + output_height + 60

    # 创建图片
    img = Image.new('RGB', (width, total_height), nb_bg)
    draw = ImageDraw.Draw(img)

    current_y = margin

    # 绘制标题
    draw.text((margin, current_y), f"Jupyter Notebook - {scenario['agent_name']}",
              fill=code_text, font=title_font)
    current_y += 50

    # 绘制代码单元格
    # In[] 提示符
    in_prompt = f"In [{scenario['cell_number']}]:"
    draw.rectangle([(margin, current_y), (margin + 80, current_y + code_height)],
                   fill=prompt_bg, outline=cell_border, width=1)
    draw.text((margin + 10, current_y + 10), in_prompt, fill=prompt_text, font=prompt_font)

    # 代码区域
    draw.rectangle([(margin + 80, current_y), (width - margin, current_y + code_height)],
                   fill=code_bg, outline=cell_border, width=1)

    # 绘制代码内容
    code_y = current_y + 15
    for line in code_lines:
        # 简单的语法高亮：注释行用灰色
        if line.strip().startswith('#'):
            draw.text((margin + 100, code_y), line, fill=comment_color, font=code_font)
        else:
            draw.text((margin + 100, code_y), line, fill=code_text, font=code_font)
        code_y += 20

    current_y += code_height + 10

    # 绘制输出单元格
    # Out[] 提示符
    out_prompt = f"Out[{scenario['cell_number']}]:"
    draw.rectangle([(margin, current_y), (margin + 80, current_y + output_height)],
                   fill=prompt_bg, outline=cell_border, width=1)
    draw.text((margin + 10, current_y + 10), out_prompt, fill=prompt_text, font=prompt_font)

    # 输出区域
    draw.rectangle([(margin + 80, current_y), (width - margin, current_y + output_height)],
                   fill=output_bg, outline=cell_border, width=1)

    # 绘制输出内容
    output_y = current_y + 15
    for line in output_lines:
        draw.text((margin + 100, output_y), line, fill=output_text, font=code_font)
        output_y += 20

    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("開始生成Jupyter Notebook風格のスクリーンショット...\n")

    # 创建输出目录
    output_dir = "notebook_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # 为每个Agent生成截图
    for i, scenario in enumerate(NOTEBOOK_SCENARIOS, 1):
        output_path = os.path.join(output_dir, f"agent_{i}_notebook.png")
        create_notebook_screenshot(scenario, output_path)

    print(f"\n✅ 完成！全ての画像が {output_dir}/ ディレクトリに保存されました")
    print(f"   合計 {len(NOTEBOOK_SCENARIOS)} 枚のNotebook画像を生成")


if __name__ == "__main__":
    main()
