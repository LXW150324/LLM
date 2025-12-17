#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Baseline实验对照组的OpenAI Playground风格截图
Baseline 1: 最基础的通用提示词
Baseline 3: 简单的角色定义
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Baseline实验对照组数据
BASELINE_CONVERSATIONS = [
    {
        "baseline_type": "Baseline 1: 最基础の汎用プロンプト",
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
        "baseline_type": "Baseline 3: シンプルな役割定義",
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
  "confidence": 0.70,
  "reasoning": "テクニカル指標は全体的に強気を示しています。価格は両方の移動平均を上回っており、上昇トレンドが確認されます。RSIは68.5で過熱気味ですが、まだ買われすぎの水準には達していません。"
}"""
    }
]


def create_baseline_playground_screenshot(conversation_data, output_path):
    """创建Baseline的OpenAI Playground风格截图（高清版）"""

    # 图片尺寸（提高分辨率）
    width = 2000
    margin = 60

    # 颜色定义（OpenAI Playground风格）
    bg_color = (255, 255, 255)  # 白色背景
    system_bg = (247, 247, 248)  # 浅灰色系统消息背景
    user_bg = (236, 253, 245)  # 浅绿色用户消息背景
    assistant_bg = (243, 244, 246)  # 浅灰色助手消息背景
    text_color = (17, 24, 39)  # 深灰色文字
    label_color = (107, 114, 128)  # 中灰色标签
    border_color = (229, 231, 235)  # 边框颜色
    baseline_color = (239, 68, 68)  # 红色标记Baseline

    # 加载字体（增大字体以提高清晰度）
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

    # 计算每个消息块的高度（增加行间距）
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

    # 总高度
    total_height = 100 + system_height + user_height + assistant_height + 150

    # 创建图片
    img = Image.new('RGB', (width, total_height), bg_color)
    draw = ImageDraw.Draw(img)

    current_y = margin

    # 绘制标题（带有Baseline标记）
    draw.text((margin, current_y), conversation_data['baseline_type'], fill=baseline_color, font=title_font)
    current_y += 70

    # 绘制System消息块（增加边框宽度）
    draw.rectangle([(margin, current_y), (width - margin, current_y + system_height)],
                   fill=system_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "SYSTEM", fill=label_color, font=label_font)

    # 绘制system提示词内容（增加行间距）
    text_y = current_y + 60
    for line in conversation_data['system_prompt'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=130) if len(line) > 130 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 30, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 30

    current_y += system_height + 30

    # 绘制User消息块
    draw.rectangle([(margin, current_y), (width - margin, current_y + user_height)],
                   fill=user_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "USER", fill=label_color, font=label_font)

    # 绘制user输入内容
    text_y = current_y + 60
    for line in conversation_data['user_input'].split('\n'):
        if line.strip():
            wrapped_lines = textwrap.wrap(line, width=130) if len(line) > 130 else [line]
            for wrapped_line in wrapped_lines:
                draw.text((margin + 30, text_y), wrapped_line, fill=text_color, font=text_font)
                text_y += 30

    current_y += user_height + 30

    # 绘制Assistant消息块
    draw.rectangle([(margin, current_y), (width - margin, current_y + assistant_height)],
                   fill=assistant_bg, outline=border_color, width=2)
    draw.text((margin + 30, current_y + 20), "ASSISTANT", fill=label_color, font=label_font)

    # 绘制assistant响应内容（JSON格式）
    text_y = current_y + 60
    for line in conversation_data['assistant_response'].split('\n'):
        draw.text((margin + 30, text_y), line, fill=text_color, font=code_font)
        text_y += 30

    # 保存图片（使用最高质量）
    img.save(output_path, 'PNG', quality=100, optimize=False, dpi=(300, 300))
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("開始生成Baseline実験対照グループの画像...\n")

    # 创建输出目录
    output_dir = "baseline_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # 为每个Baseline生成截图
    baseline_names = ["baseline1", "baseline3"]
    for i, conversation in enumerate(BASELINE_CONVERSATIONS):
        output_path = os.path.join(output_dir, f"{baseline_names[i]}_playground.png")
        create_baseline_playground_screenshot(conversation, output_path)

    print(f"\n✅ 完成！全ての画像が {output_dir}/ ディレクトリに保存されました")
    print(f"   合計 {len(BASELINE_CONVERSATIONS)} 枚のBaseline画像を生成")


if __name__ == "__main__":
    main()
