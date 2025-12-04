#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成OpenAI Playground风格的对话界面截图
模拟LLM运行时输入提示词的界面
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# 5个Agent的对话数据
CONVERSATIONS = [
    {
        "agent_name": "Agent 1: テクニカルアナリスト",
        "system_prompt": """あなたは経験豊富なテクニカルアナリストで、価格動向とテクニカル指標の分析に特化しています。

あなたの職務：
1. 価格トレンドの分析（上昇/下降/横ばい）
2. テクニカル指標の解釈（RSI、MACD、ボリンジャーバンドなど）
3. 主要なサポートレベルとレジスタンスレベルの識別
4. 売買シグナルの強度評価""",
        "user_input": """以下のAAPL株のテクニカルデータを分析してください：

現在価格: $163.50
20日移動平均: $160.20
50日移動平均: $158.80
RSI(14): 68.5
MACD: 1.25 (シグナル: 0.85)""",
        "assistant_response": """{
  "agent": "Technical Analyst",
  "stance": "bullish",
  "confidence": 0.75,
  "trend_direction": "uptrend",
  "trend_strength": "moderate",
  "reasoning": "現在価格が20日MAと50日MAの両方を上回っており、明確な上昇トレンドを示しています。RSIは68.5で過熱気味ですが、まだ買われすぎの領域（70超）には達していません。"
}"""
    },
    {
        "agent_name": "Agent 2: ファンダメンタルアナリスト",
        "system_prompt": """あなたはベテランのファンダメンタルアナリストで、企業の財務分析とバリュエーション評価に特化しています。

あなたの職務：
1. 企業の財務健全性の分析（収益性、支払能力、運営効率）
2. 企業のバリュエーションレベルの評価（PE、PB、PEGなどの指標）
3. 企業と業界平均との比較
4. 現在の価格が妥当か判断（割高/適正/割安）""",
        "user_input": """以下のAAPL株の財務データを評価してください：

現在株価: $163.50
PE比率: 28.5
PB比率: 45.2
ROE: 147.5%
営業利益率: 30.2%
売上高成長率: 8.5%""",
        "assistant_response": """{
  "agent": "Fundamental Analyst",
  "stance": "neutral",
  "confidence": 0.65,
  "valuation_assessment": "fairly_valued",
  "financial_health": "excellent",
  "reasoning": "Appleの財務状況は非常に優れており、ROE 147.5%と営業利益率30.2%は業界トップクラスです。ただしPE 28.5倍は市場平均を上回っており、成長率8.5%を考慮すると割高感があります。"
}"""
    },
    {
        "agent_name": "Agent 3: センチメントアナリスト",
        "system_prompt": """あなたはプロのマーケットセンチメントアナリストで、ソーシャルメディアのセンチメントと市場心理が株式に与える影響の分析に特化しています。

あなたの職務：
1. ソーシャルメディア（Reddit、Twitterなど）上の投資家センチメントデータの解釈
2. センチメント指標の分析（ポジティブ/ネガティブ/ニュートラルの言及数、センチメントスコアなど）
3. 市場センチメントの強度と持続性の評価""",
        "user_input": """以下のAAPL株のセンチメントデータを分析してください：

センチメントスコア: 0.72 (0=悲観的, 1=楽観的)
ポジティブ言及: 1,250回
ネガティブ言及: 380回
総議論量: 1,850回
トレンドスコア: 8.5/10""",
        "assistant_response": """{
  "agent": "Sentiment Analyst",
  "stance": "bullish",
  "confidence": 0.72,
  "sentiment_score": 0.72,
  "sentiment_strength": "strong",
  "reasoning": "センチメントスコア0.72は強い楽観的センチメントを示しています。ポジティブ言及がネガティブの3倍以上あり、高い議論量とトレンドスコアから市場の関心が高いことが分かります。"
}"""
    },
    {
        "agent_name": "Agent 4: ニュースアナリスト",
        "system_prompt": """あなたはベテランの財務ニュースアナリストで、ニュースイベントが株価に与える影響の分析に特化しています。

あなたの職務：
1. 提供された財務ニュースと経済イベントを注意深く読む
2. 各ニュースが対象株式に与える潜在的影響を評価
3. 影響の期間を判断（短期/中期/長期）
4. 総合的なニュース面での判断を提供""",
        "user_input": """以下のAAPL関連ニュースを分析してください：

1. AppleがVision Proの新バージョンを発表、価格を20%削減
2. Q3決算：売上高は予想を5%上回る、EPSも予想超え
3. CEOが2025年のAI戦略について楽観的な見通しを表明""",
        "assistant_response": """{
  "agent": "News Analyst",
  "stance": "bullish",
  "confidence": 0.80,
  "overall_sentiment": "positive",
  "key_events": [
    {"event": "Vision Pro価格削減", "impact": "positive", "timeframe": "medium"},
    {"event": "好調な決算", "impact": "positive", "timeframe": "short"},
    {"event": "AI戦略発表", "impact": "positive", "timeframe": "long"}
  ],
  "reasoning": "3つの主要なポジティブニュースが重なっており、短期・中期・長期すべての時間軸で好材料が揃っています。特に決算超えとAI戦略は投資家の信頼を高める要因です。"
}"""
    },
    {
        "agent_name": "Agent 5: トレーダー",
        "system_prompt": """あなたは経験豊富なトレーダーで、すべてのアナリストと研究者の意見を統合し、最終的な取引決定を行う責任があります。

あなたの職務：
1. すべてのアナリストのレポートを注意深く読む
2. 強気と弱気の研究者の見解を比較検討
3. リスク管理の提案を考慮
4. 明確な取引決定を行う（買い/売り/保有）""",
        "user_input": """以下の分析結果に基づいて取引決定を行ってください：

テクニカル: bullish (信頼度0.75)
ファンダメンタル: neutral (信頼度0.65)
センチメント: bullish (信頼度0.72)
ニュース: bullish (信頼度0.80)

現在価格: $163.50""",
        "assistant_response": """{
  "agent": "Trader",
  "decision": "buy",
  "confidence": 0.73,
  "position_size": 0.6,
  "entry_price": 163.50,
  "stop_loss": 158.00,
  "take_profit": 172.00,
  "consensus_level": "high",
  "reasoning": "4つの分析のうち3つが強気、1つが中立であり、コンセンサスレベルは高いです。テクニカル、センチメント、ニュースすべてが買いシグナルを示しており、ファンダメンタルも売りではありません。60%のポジションサイズで買い推奨、ストップロスは直近のサポートレベル$158に設定します。"
}"""
    }
]


def create_playground_screenshot(conversation_data, output_path):
    """创建OpenAI Playground风格的对话界面截图"""

    # 图片尺寸
    width = 1400
    margin = 40

    # 颜色定义（OpenAI Playground风格）
    bg_color = (255, 255, 255)  # 白色背景
    system_bg = (247, 247, 248)  # 浅灰色系统消息背景
    user_bg = (236, 253, 245)  # 浅绿色用户消息背景
    assistant_bg = (243, 244, 246)  # 浅灰色助手消息背景
    text_color = (17, 24, 39)  # 深灰色文字
    label_color = (107, 114, 128)  # 中灰色标签
    border_color = (229, 231, 235)  # 边框颜色

    # 加载字体
    try:
        japanese_font = "/usr/share/fonts/truetype/custom/NotoSansJP.ttf"
        title_font = ImageFont.truetype(japanese_font, 18)
        label_font = ImageFont.truetype(japanese_font, 14)
        text_font = ImageFont.truetype(japanese_font, 13)
        code_font = ImageFont.truetype(japanese_font, 12)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # 计算每个消息块的高度
    def calculate_text_height(text, font, max_width):
        lines = []
        for paragraph in text.split('\n'):
            if len(paragraph) <= 100:
                lines.append(paragraph)
            else:
                lines.extend(textwrap.wrap(paragraph, width=100))
        return len(lines) * 22 + 40

    system_height = calculate_text_height(conversation_data['system_prompt'], text_font, width - 2*margin - 40)
    user_height = calculate_text_height(conversation_data['user_input'], text_font, width - 2*margin - 40)
    assistant_height = calculate_text_height(conversation_data['assistant_response'], code_font, width - 2*margin - 40)

    # 总高度
    total_height = 80 + system_height + user_height + assistant_height + 100

    # 创建图片
    img = Image.new('RGB', (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    current_y = margin

    # 绘制标题
    draw.text((margin, current_y), conversation_data['agent_name'], fill=text_color, font=title_font)
    current_y += 50

    # 绘制System消息块
    draw.rectangle([(margin, current_y), (width - margin, current_y + system_height)],
                   fill=system_bg, outline=border_color, width=1)
    draw.text((margin + 20, current_y + 15), "SYSTEM", fill=label_color, font=label_font)

    # 绘制system提示词内容
    text_y = current_y + 45
    for line in conversation_data['system_prompt'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=100) if len(line) > 100 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 20, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 22

    current_y += system_height + 20

    # 绘制User消息块
    draw.rectangle([(margin, current_y), (width - margin, current_y + user_height)],
                   fill=user_bg, outline=border_color, width=1)
    draw.text((margin + 20, current_y + 15), "USER", fill=label_color, font=label_font)

    # 绘制user输入内容
    text_y = current_y + 45
    for line in conversation_data['user_input'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=100) if len(line) > 100 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 20, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 22

    current_y += user_height + 20

    # 绘制Assistant消息块
    draw.rectangle([(margin, current_y), (width - margin, current_y + assistant_height)],
                   fill=assistant_bg, outline=border_color, width=1)
    draw.text((margin + 20, current_y + 15), "ASSISTANT", fill=label_color, font=label_font)

    # 绘制assistant响应内容（JSON格式）
    text_y = current_y + 45
    for line in conversation_data['assistant_response'].split('\n'):
        draw.text((margin + 20, text_y), line, fill=text_color, font=code_font)
        text_y += 22

    # 保存图片
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("開始生成OpenAI Playground風格の対話画像...\n")

    # 创建输出目录
    output_dir = "playground_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # 为每个Agent生成截图
    for i, conversation in enumerate(CONVERSATIONS, 1):
        output_path = os.path.join(output_dir, f"agent_{i}_playground.png")
        create_playground_screenshot(conversation, output_path)

    print(f"\n✅ 完成！全ての画像が {output_dir}/ ディレクトリに保存されました")
    print(f"   合計 {len(CONVERSATIONS)} 枚の対話画像を生成")


if __name__ == "__main__":
    main()
