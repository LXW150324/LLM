#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的Baseline实验对照组截图
Baseline 1: 最基础的通用提示词 (5个Agent)
Baseline 3: 简单的角色定义 (5个Agent)
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Baseline 1: 最基础的通用提示词（5个Agent）
BASELINE1_CONVERSATIONS = [
    {
        "agent_name": "Baseline 1 - Agent 1: テクニカル分析",
        "system_prompt": """株式市場アナリストとして、提供された株式データを分析し、取引推奨を提供してください。

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "簡潔な説明"
}""",
        "user_input": """以下のAAPL株のテクニカルデータを分析してください：

現在価格: $163.50
20日移動平均: $160.20
50日移動平均: $158.80
RSI(14): 68.5
MACD: 1.25 (シグナル: 0.85)""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.68,
  "reasoning": "価格が移動平均を上回っており、RSIは強気圏にあります。MACDもポジティブなシグナルを示しています。"
}"""
    },
    {
        "agent_name": "Baseline 1 - Agent 2: ファンダメンタル分析",
        "system_prompt": """株式市場アナリストとして、提供された株式データを分析し、取引推奨を提供してください。

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "簡潔な説明"
}""",
        "user_input": """以下のAAPL株の財務データを評価してください：

現在株価: $163.50
PE比率: 28.5
PB比率: 45.2
ROE: 147.5%
営業利益率: 30.2%
売上高成長率: 8.5%""",
        "assistant_response": """{
  "stance": "neutral",
  "confidence": 0.60,
  "reasoning": "財務指標は良好ですが、PE比率が高く、成長率は減速しています。"
}"""
    },
    {
        "agent_name": "Baseline 1 - Agent 3: センチメント分析",
        "system_prompt": """株式市場アナリストとして、提供された株式データを分析し、取引推奨を提供してください。

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "簡潔な説明"
}""",
        "user_input": """以下のAAPL株のセンチメントデータを分析してください：

センチメントスコア: 0.72 (0=悲観的, 1=楽観的)
ポジティブ言及: 1,250回
ネガティブ言及: 380回
総議論量: 1,850回
トレンドスコア: 8.5/10""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.70,
  "reasoning": "センチメントスコアが高く、ポジティブな言及が多いです。"
}"""
    },
    {
        "agent_name": "Baseline 1 - Agent 4: ニュース分析",
        "system_prompt": """株式市場アナリストとして、提供された株式データを分析し、取引推奨を提供してください。

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "簡潔な説明"
}""",
        "user_input": """以下のAAPL関連ニュースを分析してください：

1. AppleがVision Proの新バージョンを発表、価格を20%削減
2. Q3決算：売上高は予想を5%上回る、EPSも予想超え
3. CEOが2025年のAI戦略について楽観的な見通しを表明""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.75,
  "reasoning": "複数のポジティブなニュースがあり、決算も良好です。"
}"""
    },
    {
        "agent_name": "Baseline 1 - Agent 5: トレーダー",
        "system_prompt": """株式市場アナリストとして、提供された株式データを分析し、取引推奨を提供してください。

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "簡潔な説明"
}""",
        "user_input": """以下の分析結果に基づいて取引決定を行ってください：

テクニカル: bullish (信頼度0.68)
ファンダメンタル: neutral (信頼度0.60)
センチメント: bullish (信頼度0.70)
ニュース: bullish (信頼度0.75)

現在価格: $163.50""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.68,
  "reasoning": "大部分の分析が強気を示しているため、買い推奨です。"
}"""
    }
]

# Baseline 3: 簡単な役色定義（5個Agent）
BASELINE3_CONVERSATIONS = [
    {
        "agent_name": "Baseline 3 - Agent 1: テクニカル分析",
        "system_prompt": """あなたは株式市場分析を専門とするテクニカルアナリストです。

あなたの役割：
- 価格トレンドとテクニカル指標を分析する
- 買い/売り/保有の推奨を提供する
- 市場状況を評価する

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "あなたの分析"
}""",
        "user_input": """以下のAAPL株のテクニカルデータを分析してください：

現在価格: $163.50
20日移動平均: $160.20
50日移動平均: $158.80
RSI(14): 68.5
MACD: 1.25 (シグナル: 0.85)""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.72,
  "reasoning": "テクニカル指標は全体的に強気を示しています。価格は両方の移動平均を上回っており、上昇トレンドが確認されます。RSIは68.5で過熱気味ですが、まだ買われすぎの水準には達していません。"
}"""
    },
    {
        "agent_name": "Baseline 3 - Agent 2: ファンダメンタル分析",
        "system_prompt": """あなたはファンダメンタル分析を専門とするアナリストです。

あなたの役割：
- 企業の財務状況を評価する
- バリュエーション分析を行う
- 投資判断を提供する

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "あなたの分析"
}""",
        "user_input": """以下のAAPL株の財務データを評価してください：

現在株価: $163.50
PE比率: 28.5
PB比率: 45.2
ROE: 147.5%
営業利益率: 30.2%
売上高成長率: 8.5%""",
        "assistant_response": """{
  "stance": "neutral",
  "confidence": 0.63,
  "reasoning": "ROEと利益率は優秀ですが、PE比率が高く割高感があります。成長率8.5%を考慮すると、現在の株価は適正と判断します。"
}"""
    },
    {
        "agent_name": "Baseline 3 - Agent 3: センチメント分析",
        "system_prompt": """あなたは市場センチメント分析を専門とするアナリストです。

あなたの役割：
- 投資家心理を分析する
- ソーシャルメディアデータを評価する
- センチメントトレンドを判断する

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "あなたの分析"
}""",
        "user_input": """以下のAAPL株のセンチメントデータを分析してください：

センチメントスコア: 0.72 (0=悲観的, 1=楽観的)
ポジティブ言及: 1,250回
ネガティブ言及: 380回
総議論量: 1,850回
トレンドスコア: 8.5/10""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.71,
  "reasoning": "センチメントスコア0.72は強い楽観を示しています。ポジティブ/ネガティブ比率が3.3:1と良好で、高い議論量から市場の関心が高いことが分かります。"
}"""
    },
    {
        "agent_name": "Baseline 3 - Agent 4: ニュース分析",
        "system_prompt": """あなたは財務ニュース分析を専門とするアナリストです。

あなたの役割：
- ニュースイベントの影響を評価する
- 企業発表を分析する
- 市場へのインパクトを判断する

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "あなたの分析"
}""",
        "user_input": """以下のAAPL関連ニュースを分析してください：

1. AppleがVision Proの新バージョンを発表、価格を20%削減
2. Q3決算：売上高は予想を5%上回る、EPSも予想超え
3. CEOが2025年のAI戦略について楽観的な見通しを表明""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.78,
  "reasoning": "3つの主要なポジティブニュースが重なっています。決算超え、製品戦略の改善、AI戦略の明確化により、短期・中期・長期すべての時間軸で好材料が揃っています。"
}"""
    },
    {
        "agent_name": "Baseline 3 - Agent 5: トレーダー",
        "system_prompt": """あなたは取引決定を専門とするトレーダーです。

あなたの役割：
- 全ての分析を統合する
- 最終的な取引判断を行う
- リスクとリターンを評価する

以下のフィールドを含むJSON形式で分析結果を出力してください：
{
    "stance": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "reasoning": "あなたの分析"
}""",
        "user_input": """以下の分析結果に基づいて取引決定を行ってください：

テクニカル: bullish (信頼度0.72)
ファンダメンタル: neutral (信頼度0.63)
センチメント: bullish (信頼度0.71)
ニュース: bullish (信頼度0.78)

現在価格: $163.50""",
        "assistant_response": """{
  "stance": "bullish",
  "confidence": 0.71,
  "reasoning": "4つの分析のうち3つが強気、1つが中立であり、コンセンサスレベルは高いです。ファンダメンタルも反対シグナルではないため、買い推奨とします。"
}"""
    }
]


def create_baseline_screenshot(conversation_data, output_path):
    """创建Baseline截图（高清版）"""

    width = 2000
    margin = 60

    bg_color = (255, 255, 255)
    system_bg = (247, 247, 248)
    user_bg = (236, 253, 245)
    assistant_bg = (243, 244, 246)
    text_color = (17, 24, 39)
    label_color = (107, 114, 128)
    border_color = (229, 231, 235)
    baseline_color = (239, 68, 68)

    try:
        japanese_font = "/usr/share/fonts/truetype/custom/NotoSansJP.ttf"
        title_font = ImageFont.truetype(japanese_font, 26)
        label_font = ImageFont.truetype(japanese_font, 20)
        text_font = ImageFont.truetype(japanese_font, 18)
        code_font = ImageFont.truetype(japanese_font, 17)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    def calculate_text_height(text, font, max_width):
        lines = []
        for paragraph in text.split('\n'):
            if len(paragraph) <= 130:
                lines.append(paragraph)
            else:
                lines.extend(textwrap.wrap(paragraph, width=130))
        return len(lines) * 30 + 60

    system_height = calculate_text_height(conversation_data['system_prompt'], text_font, width - 2*margin - 40)
    user_height = calculate_text_height(conversation_data['user_input'], text_font, width - 2*margin - 40)
    assistant_height = calculate_text_height(conversation_data['assistant_response'], code_font, width - 2*margin - 40)

    total_height = 100 + system_height + user_height + assistant_height + 150

    img = Image.new('RGB', (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    current_y = margin

    draw.text((margin, current_y), conversation_data['agent_name'], fill=baseline_color, font=title_font)
    current_y += 70

    draw.rectangle([(margin, current_y), (width - margin, current_y + system_height)],
                   fill=system_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "SYSTEM", fill=label_color, font=label_font)

    text_y = current_y + 60
    for line in conversation_data['system_prompt'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=130) if len(line) > 130 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 30, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 30

    current_y += system_height + 30

    draw.rectangle([(margin, current_y), (width - margin, current_y + user_height)],
                   fill=user_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "USER", fill=label_color, font=label_font)

    text_y = current_y + 60
    for line in conversation_data['user_input'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=130) if len(line) > 130 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 30, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 30

    current_y += user_height + 30

    draw.rectangle([(margin, current_y), (width - margin, current_y + assistant_height)],
                   fill=assistant_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "ASSISTANT", fill=label_color, font=label_font)

    text_y = current_y + 60
    for line in conversation_data['assistant_response'].split('\n'):
        draw.text((margin + 30, text_y), line, fill=text_color, font=code_font)
        text_y += 30

    img.save(output_path, 'PNG', quality=100, optimize=False, dpi=(300, 300))
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("開始生成完整なBaseline実験画像（各5枚）...\n")

    output_dir = "baseline_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    print("=== Baseline 1を生成中 ===")
    for i, conversation in enumerate(BASELINE1_CONVERSATIONS, 1):
        output_path = os.path.join(output_dir, f"baseline1_agent{i}_playground.png")
        create_baseline_screenshot(conversation, output_path)

    print("\n=== Baseline 3を生成中 ===")
    for i, conversation in enumerate(BASELINE3_CONVERSATIONS, 1):
        output_path = os.path.join(output_dir, f"baseline3_agent{i}_playground.png")
        create_baseline_screenshot(conversation, output_path)

    print(f"\n✅ 完成！全ての画像が {output_dir}/ ディレクトリに保存されました")
    print(f"   Baseline 1: {len(BASELINE1_CONVERSATIONS)} 枚")
    print(f"   Baseline 3: {len(BASELINE3_CONVERSATIONS)} 枚")
    print(f"   合計: {len(BASELINE1_CONVERSATIONS) + len(BASELINE3_CONVERSATIONS)} 枚")


if __name__ == "__main__":
    main()
