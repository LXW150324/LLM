#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的多Agent交易系统运行界面截图
展示5个Agent协同工作的完整流程
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_full_system_screenshot(output_path):
    """创建完整系统运行界面截图"""

    # 图片尺寸
    width = 2000
    height = 2800
    margin = 50

    # 颜色定义
    bg_color = (18, 18, 18)  # 深色背景
    panel_bg = (30, 30, 30)  # 面板背景
    header_bg = (45, 45, 45)  # 标题背景
    success_color = (34, 197, 94)  # 绿色（成功）
    info_color = (59, 130, 246)  # 蓝色（信息）
    warning_color = (251, 191, 36)  # 黄色（警告）
    text_color = (229, 229, 229)  # 浅色文字
    dim_text = (156, 163, 175)  # 暗色文字
    border_color = (75, 85, 99)  # 边框颜色

    # 加载字体
    try:
        japanese_font = "/usr/share/fonts/truetype/custom/NotoSansJP.ttf"
        title_font = ImageFont.truetype(japanese_font, 32)
        subtitle_font = ImageFont.truetype(japanese_font, 22)
        text_font = ImageFont.truetype(japanese_font, 18)
        small_font = ImageFont.truetype(japanese_font, 16)
        code_font = ImageFont.truetype(japanese_font, 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # 创建图片
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    current_y = margin

    # ========== 系统标题 ==========
    draw.text((margin, current_y), "🤖 マルチエージェント株式取引システム",
              fill=text_color, font=title_font)
    current_y += 50
    draw.text((margin, current_y), "Multi-Agent Stock Trading System - 実行中...",
              fill=dim_text, font=small_font)
    current_y += 60

    # ========== 系统初始化 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 120)],
                   fill=panel_bg, outline=border_color, width=2)
    draw.text((margin + 20, current_y + 15), "📊 システム初期化",
              fill=info_color, font=subtitle_font)

    init_y = current_y + 50
    draw.text((margin + 30, init_y), "✓ データソース接続完了", fill=success_color, font=text_font)
    draw.text((margin + 30, init_y + 30), "✓ 5つのエージェント初期化完了", fill=success_color, font=text_font)
    draw.text((margin + 30, init_y + 60), "✓ 分析対象: AAPL (Apple Inc.) - 現在価格: $163.50",
              fill=success_color, font=text_font)

    current_y += 140

    # ========== Agent 1: 技術分析 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 200)],
                   fill=panel_bg, outline=border_color, width=2)
    draw.rectangle([(margin, current_y), (width - margin, current_y + 45)],
                   fill=header_bg, outline=border_color, width=2)
    draw.text((margin + 20, current_y + 10), "Agent 1: テクニカルアナリスト [実行完了 ✓]",
              fill=success_color, font=subtitle_font)

    agent1_y = current_y + 60
    draw.text((margin + 30, agent1_y), "分析結果:", fill=text_color, font=text_font)
    draw.text((margin + 50, agent1_y + 30), '• スタンス: Bullish (強気)', fill=text_color, font=text_font)
    draw.text((margin + 50, agent1_y + 60), '• 信頼度: 0.75', fill=text_color, font=text_font)
    draw.text((margin + 50, agent1_y + 90), '• トレンド: 上昇トレンド (中程度の強さ)', fill=text_color, font=text_font)
    draw.text((margin + 50, agent1_y + 120), '• 主要シグナル: RSI 68.5, MACD 1.25 (強気)', fill=text_color, font=text_font)

    current_y += 220

    # ========== Agent 2: ファンダメンタル分析 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 200)],
                   fill=panel_bg, outline=border_color, width=2)
    draw.rectangle([(margin, current_y), (width - margin, current_y + 45)],
                   fill=header_bg, outline=border_color, width=2)
    draw.text((margin + 20, current_y + 10), "Agent 2: ファンダメンタルアナリスト [実行完了 ✓]",
              fill=success_color, font=subtitle_font)

    agent2_y = current_y + 60
    draw.text((margin + 30, agent2_y), "分析結果:", fill=text_color, font=text_font)
    draw.text((margin + 50, agent2_y + 30), '• スタンス: Neutral (中立)', fill=warning_color, font=text_font)
    draw.text((margin + 50, agent2_y + 60), '• 信頼度: 0.65', fill=text_color, font=text_font)
    draw.text((margin + 50, agent2_y + 90), '• バリュエーション: 適正価格', fill=text_color, font=text_font)
    draw.text((margin + 50, agent2_y + 120), '• 財務健全性: 優秀 (ROE 147.5%, 利益率 30.2%)',
              fill=text_color, font=text_font)

    current_y += 220

    # ========== Agent 3: センチメント分析 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 200)],
                   fill=panel_bg, outline=border_color, width=2)
    draw.rectangle([(margin, current_y), (width - margin, current_y + 45)],
                   fill=header_bg, outline=border_color, width=2)
    draw.text((margin + 20, current_y + 10), "Agent 3: センチメントアナリスト [実行完了 ✓]",
              fill=success_color, font=subtitle_font)

    agent3_y = current_y + 60
    draw.text((margin + 30, agent3_y), "分析結果:", fill=text_color, font=text_font)
    draw.text((margin + 50, agent3_y + 30), '• スタンス: Bullish (強気)', fill=text_color, font=text_font)
    draw.text((margin + 50, agent3_y + 60), '• 信頼度: 0.72', fill=text_color, font=text_font)
    draw.text((margin + 50, agent3_y + 90), '• センチメントスコア: 0.72 (強い楽観)', fill=text_color, font=text_font)
    draw.text((margin + 50, agent3_y + 120), '• ポジティブ/ネガティブ比率: 3.3:1', fill=text_color, font=text_font)

    current_y += 220

    # ========== Agent 4: ニュース分析 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 200)],
                   fill=panel_bg, outline=border_color, width=2)
    draw.rectangle([(margin, current_y), (width - margin, current_y + 45)],
                   fill=header_bg, outline=border_color, width=2)
    draw.text((margin + 20, current_y + 10), "Agent 4: ニュースアナリスト [実行完了 ✓]",
              fill=success_color, font=subtitle_font)

    agent4_y = current_y + 60
    draw.text((margin + 30, agent4_y), "分析結果:", fill=text_color, font=text_font)
    draw.text((margin + 50, agent4_y + 30), '• スタンス: Bullish (強気)', fill=text_color, font=text_font)
    draw.text((margin + 50, agent4_y + 60), '• 信頼度: 0.80', fill=text_color, font=text_font)
    draw.text((margin + 50, agent4_y + 90), '• 主要イベント: Vision Pro価格削減、決算超え、AI戦略',
              fill=text_color, font=text_font)
    draw.text((margin + 50, agent4_y + 120), '• 総合センチメント: Positive (3つの好材料)',
              fill=text_color, font=text_font)

    current_y += 220

    # ========== Agent 5: 最終決定 ==========
    draw.rectangle([(margin, current_y), (width - margin, current_y + 280)],
                   fill=(25, 60, 25), outline=success_color, width=3)  # 绿色边框表示买入
    draw.rectangle([(margin, current_y), (width - margin, current_y + 45)],
                   fill=header_bg, outline=success_color, width=3)
    draw.text((margin + 20, current_y + 10), "Agent 5: トレーダー [最終判断 ✓]",
              fill=success_color, font=subtitle_font)

    trader_y = current_y + 60
    draw.text((margin + 30, trader_y), "🎯 取引決定:", fill=success_color, font=subtitle_font)
    draw.text((margin + 50, trader_y + 40), '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
              fill=border_color, font=text_font)
    draw.text((margin + 50, trader_y + 70), '決定: BUY (買い)', fill=success_color, font=title_font)
    draw.text((margin + 50, trader_y + 110), '信頼度: 0.73 | ポジションサイズ: 60%', fill=text_color, font=text_font)
    draw.text((margin + 50, trader_y + 140), 'エントリー価格: $163.50', fill=text_color, font=text_font)
    draw.text((margin + 50, trader_y + 170), 'ストップロス: $158.00 | 利益確定: $172.00',
              fill=text_color, font=text_font)
    draw.text((margin + 50, trader_y + 200), 'コンセンサスレベル: HIGH (4つ中3つが強気)',
              fill=text_color, font=text_font)

    # 保存图片
    img.save(output_path, 'PNG', quality=100, optimize=False, dpi=(300, 300))
    print(f"✓ 已生成: {output_path}")


def main():
    """主函数"""
    print("開始生成完整システム実行画面...\n")

    # 创建输出目录
    output_dir = "system_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    # 生成完整系统运行截图
    output_path = os.path.join(output_dir, "full_system_execution.png")
    create_full_system_screenshot(output_path)

    print(f"\n✅ 完成！画像が {output_dir}/ ディレクトリに保存されました")


if __name__ == "__main__":
    main()
