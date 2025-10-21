"""
简化版数据处理模块
使用pandas直接计算技术指标，不依赖ta库
"""

import pandas as pd
import numpy as np
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

from config.config import config

class DataProcessor:
    """简化版数据处理器"""

    def __init__(self):
        """初始化数据处理器"""
        self.tech_config = config.TECHNICAL_INDICATORS

    def calculate_sma(self, series, window):
        """计算简单移动平均"""
        return series.rolling(window=window).mean()

    def calculate_ema(self, series, span):
        """计算指数移动平均"""
        return series.ewm(span=span, adjust=False).mean()

    def calculate_rsi(self, series, period=14):
        """计算RSI指标"""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_macd(self, series, fast=12, slow=26, signal=9):
        """计算MACD指标"""
        ema_fast = self.calculate_ema(series, fast)
        ema_slow = self.calculate_ema(series, slow)
        macd = ema_fast - ema_slow
        macd_signal = self.calculate_ema(macd, signal)
        macd_diff = macd - macd_signal
        return macd, macd_signal, macd_diff

    def calculate_bollinger_bands(self, series, window=20, num_std=2):
        """计算布林带"""
        sma = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, sma, lower_band

    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算技术指标

        Args:
            df: 包含OHLCV数据的DataFrame

        Returns:
            添加了技术指标的DataFrame
        """
        print("📊 正在计算技术指标...")

        if df.empty:
            return df

        df = df.copy()

        try:
            # 移动平均线
            df['sma_short'] = self.calculate_sma(df['close'], self.tech_config['SMA_SHORT'])
            df['sma_long'] = self.calculate_sma(df['close'], self.tech_config['SMA_LONG'])

            # 指数移动平均
            df['ema_12'] = self.calculate_ema(df['close'], 12)
            df['ema_26'] = self.calculate_ema(df['close'], 26)

            # MACD
            df['macd'], df['macd_signal'], df['macd_diff'] = self.calculate_macd(
                df['close'],
                self.tech_config['MACD_FAST'],
                self.tech_config['MACD_SLOW'],
                self.tech_config['MACD_SIGNAL']
            )

            # RSI
            df['rsi'] = self.calculate_rsi(df['close'], self.tech_config['RSI_PERIOD'])

            # 布林带
            df['bb_upper'], df['bb_middle'], df['bb_lower'] = self.calculate_bollinger_bands(
                df['close'],
                self.tech_config['BB_PERIOD'],
                self.tech_config['BB_STD']
            )
            df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']

            # 价格变化百分比
            df['price_change'] = df['close'].pct_change() * 100

            # 成交量变化率
            df['volume_change'] = df['volume'].pct_change() * 100

            print("✅ 技术指标计算完成")

        except Exception as e:
            print(f"⚠️  计算技术指标时出错: {str(e)}")

        return df

    def generate_technical_summary(self, df: pd.DataFrame, date: str) -> Dict:
        """
        生成技术分析摘要

        Args:
            df: 包含技术指标的DataFrame
            date: 目标日期

        Returns:
            技术分析摘要字典
        """
        try:
            # 转换日期格式
            date_obj = pd.to_datetime(date)

            if date_obj not in df.index:
                # 找到最接近的日期
                closest_date = df.index[df.index <= date_obj].max()
                if pd.isna(closest_date):
                    closest_date = df.index[0]
                date_obj = closest_date

            row = df.loc[date_obj]

            # 构建技术摘要
            summary = {
                'date': date_obj.strftime('%Y-%m-%d'),
                'price': {
                    'current': float(row['close']),
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'change_pct': float(row.get('price_change', 0))
                },
                'volume': {
                    'current': int(row['volume']),
                    'change_pct': float(row.get('volume_change', 0))
                },
                'moving_averages': {
                    'sma_20': float(row.get('sma_short', 0)),
                    'sma_50': float(row.get('sma_long', 0)),
                    'ema_12': float(row.get('ema_12', 0)),
                    'ema_26': float(row.get('ema_26', 0))
                },
                'momentum': {
                    'rsi': float(row.get('rsi', 50)),
                    'macd': float(row.get('macd', 0)),
                    'macd_signal': float(row.get('macd_signal', 0)),
                    'macd_diff': float(row.get('macd_diff', 0))
                },
                'volatility': {
                    'bb_upper': float(row.get('bb_upper', 0)),
                    'bb_middle': float(row.get('bb_middle', 0)),
                    'bb_lower': float(row.get('bb_lower', 0)),
                    'bb_width': float(row.get('bb_width', 0))
                }
            }

            return summary

        except Exception as e:
            print(f"⚠️  生成技术摘要时出错: {str(e)}")
            return {
                'date': date,
                'price': {'current': 0, 'open': 0, 'high': 0, 'low': 0, 'change_pct': 0},
                'volume': {'current': 0, 'change_pct': 0},
                'moving_averages': {'sma_20': 0, 'sma_50': 0, 'ema_12': 0, 'ema_26': 0},
                'momentum': {'rsi': 50, 'macd': 0, 'macd_signal': 0, 'macd_diff': 0},
                'volatility': {'bb_upper': 0, 'bb_middle': 0, 'bb_lower': 0, 'bb_width': 0}
            }
