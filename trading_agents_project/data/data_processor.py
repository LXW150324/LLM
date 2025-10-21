"""
数据处理模块
负责计算技术指标、数据清洗、特征工程等
"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

from config.config import config

class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        """初始化数据处理器"""
        self.tech_config = config.TECHNICAL_INDICATORS
    
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
            df['sma_short'] = ta.trend.sma_indicator(
                df['close'], 
                window=self.tech_config['SMA_SHORT']
            )
            df['sma_long'] = ta.trend.sma_indicator(
                df['close'], 
                window=self.tech_config['SMA_LONG']
            )
            
            # 指数移动平均
            df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
            df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
            
            # MACD
            macd = ta.trend.MACD(
                df['close'],
                window_fast=self.tech_config['MACD_FAST'],
                window_slow=self.tech_config['MACD_SLOW'],
                window_sign=self.tech_config['MACD_SIGNAL']
            )
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()
            
            # RSI
            df['rsi'] = ta.momentum.rsi(
                df['close'], 
                window=self.tech_config['RSI_PERIOD']
            )
            
            # 布林带
            bollinger = ta.volatility.BollingerBands(
                df['close'],
                window=self.tech_config['BB_PERIOD'],
                window_dev=self.tech_config['BB_STD']
            )
            df['bb_upper'] = bollinger.bollinger_hband()
            df['bb_middle'] = bollinger.bollinger_mavg()
            df['bb_lower'] = bollinger.bollinger_lband()
            df['bb_width'] = bollinger.bollinger_wband()
            
            # ATR (平均真实波幅)
            df['atr'] = ta.volatility.average_true_range(
                df['high'], df['low'], df['close'], window=14
            )
            
            # OBV (能量潮)
            df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
            
            # 随机指标
            stoch = ta.momentum.StochasticOscillator(
                df['high'], df['low'], df['close']
            )
            df['stoch_k'] = stoch.stoch()
            df['stoch_d'] = stoch.stoch_signal()
            
            # ADX (平均趋向指数)
            df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14)
            
            # 成交量变化率
            df['volume_change'] = df['volume'].pct_change()
            
            # 价格动量
            df['momentum'] = df['close'].pct_change(periods=10)
            
            # 填充NaN值
            df = df.fillna(method='bfill').fillna(method='ffill')
            
            print(f"✅ 成功计算 {len([c for c in df.columns if c not in ['open', 'high', 'low', 'close', 'volume', 'symbol']])} 个技术指标")
            
        except Exception as e:
            print(f"❌ 计算技术指标时出错: {str(e)}")
        
        return df
    
    def generate_technical_summary(self, df: pd.DataFrame, current_date: str = None) -> Dict:
        """
        生成技术分析摘要
        
        Args:
            df: 包含技术指标的DataFrame
            current_date: 当前日期（用于获取特定日期的数据）
            
        Returns:
            技术分析摘要字典
        """
        if df.empty:
            return {}
        
        if current_date:
            try:
                current_data = df.loc[current_date]
            except:
                current_data = df.iloc[-1]
        else:
            current_data = df.iloc[-1]
        
        summary = {
            'price': {
                'current': float(current_data['close']),
                'open': float(current_data['open']),
                'high': float(current_data['high']),
                'low': float(current_data['low']),
                'volume': int(current_data['volume']),
                'change_pct': float(current_data['returns'] * 100) if 'returns' in current_data else 0,
            },
            'trend': {
                'sma_short': float(current_data['sma_short']),
                'sma_long': float(current_data['sma_long']),
                'ema_12': float(current_data['ema_12']),
                'ema_26': float(current_data['ema_26']),
                'trend_direction': 'bullish' if current_data['sma_short'] > current_data['sma_long'] else 'bearish',
            },
            'momentum': {
                'rsi': float(current_data['rsi']),
                'rsi_signal': self._get_rsi_signal(current_data['rsi']),
                'macd': float(current_data['macd']),
                'macd_signal': float(current_data['macd_signal']),
                'macd_histogram': float(current_data['macd_diff']),
                'stoch_k': float(current_data['stoch_k']),
                'stoch_d': float(current_data['stoch_d']),
            },
            'volatility': {
                'bb_upper': float(current_data['bb_upper']),
                'bb_middle': float(current_data['bb_middle']),
                'bb_lower': float(current_data['bb_lower']),
                'bb_width': float(current_data['bb_width']),
                'atr': float(current_data['atr']),
                'position': self._get_bb_position(
                    current_data['close'],
                    current_data['bb_upper'],
                    current_data['bb_middle'],
                    current_data['bb_lower']
                ),
            },
            'volume': {
                'obv': float(current_data['obv']),
                'volume_change_pct': float(current_data['volume_change'] * 100) if not pd.isna(current_data['volume_change']) else 0,
            },
            'strength': {
                'adx': float(current_data['adx']),
                'trend_strength': self._get_trend_strength(current_data['adx']),
            }
        }
        
        return summary
    
    @staticmethod
    def _get_rsi_signal(rsi: float) -> str:
        """获取RSI信号"""
        if rsi > 70:
            return 'overbought'
        elif rsi < 30:
            return 'oversold'
        else:
            return 'neutral'
    
    @staticmethod
    def _get_bb_position(price: float, upper: float, middle: float, lower: float) -> str:
        """获取价格在布林带中的位置"""
        if price > upper:
            return 'above_upper'
        elif price < lower:
            return 'below_lower'
        elif price > middle:
            return 'upper_half'
        else:
            return 'lower_half'
    
    @staticmethod
    def _get_trend_strength(adx: float) -> str:
        """获取趋势强度"""
        if adx > 50:
            return 'very_strong'
        elif adx > 25:
            return 'strong'
        elif adx > 20:
            return 'moderate'
        else:
            return 'weak'
    
    def prepare_training_data(self, df: pd.DataFrame, lookback: int = 60) -> pd.DataFrame:
        """
        准备训练数据，添加历史窗口特征
        
        Args:
            df: 原始数据
            lookback: 回看窗口大小
            
        Returns:
            处理后的DataFrame
        """
        print(f"🔄 正在准备训练数据 (回看窗口={lookback})...")
        
        df = df.copy()
        
        # 添加滞后特征
        for lag in [1, 5, 10, 20]:
            df[f'returns_lag_{lag}'] = df['returns'].shift(lag)
            df[f'volume_lag_{lag}'] = df['volume'].shift(lag)
        
        # 添加滚动统计特征
        for window in [5, 10, 20]:
            df[f'returns_mean_{window}'] = df['returns'].rolling(window).mean()
            df[f'returns_std_{window}'] = df['returns'].rolling(window).std()
            df[f'volume_mean_{window}'] = df['volume'].rolling(window).mean()
        
        # 删除NaN行
        df = df.dropna()
        
        print(f"✅ 训练数据准备完成，共 {len(df)} 行")
        return df

# 示例使用
if __name__ == "__main__":
    from data.data_collector import DataCollector
    
    collector = DataCollector(['AAPL'])
    data = collector.collect_stock_data('AAPL', '2023-01-01', '2024-01-01')
    
    processor = DataProcessor()
    data_with_indicators = processor.calculate_technical_indicators(data)
    
    print("\n数据列:")
    print(data_with_indicators.columns.tolist())
    
    print("\n技术分析摘要:")
    summary = processor.generate_technical_summary(data_with_indicators)
    import json
    print(json.dumps(summary, indent=2))