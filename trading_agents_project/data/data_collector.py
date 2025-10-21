"""
数据收集模块
负责从各种来源获取股票数据、新闻、社交媒体情绪等
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

from config.config import config

class DataCollector:
    """数据收集器"""
    
    def __init__(self, symbols: List[str] = None):
        """
        初始化数据收集器
        
        Args:
            symbols: 股票代码列表
        """
        self.symbols = symbols or config.STOCK_SYMBOLS
        self.data_cache = {}
        
    def collect_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        收集股票价格数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            包含股票价格数据的DataFrame
        """
        print(f"📈 正在获取 {symbol} 的价格数据...")
        
        try:
            # 使用yfinance获取数据
            stock = yf.Ticker(symbol)
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                print(f"⚠️  {symbol} 没有数据")
                return pd.DataFrame()
            
            # 重命名列
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # 添加股票代码
            df['symbol'] = symbol
            
            # 计算每日收益率
            df['returns'] = df['close'].pct_change()
            
            # 计算价格方向 (1=上涨, 0=下跌)
            df['direction'] = (df['returns'] > 0).astype(int)
            
            print(f"✅ 成功获取 {len(df)} 条数据")
            return df
            
        except Exception as e:
            print(f"❌ 获取 {symbol} 数据失败: {str(e)}")
            return pd.DataFrame()
    
    def collect_financial_data(self, symbol: str) -> Dict:
        """
        收集基本面财务数据
        
        Args:
            symbol: 股票代码
            
        Returns:
            财务数据字典
        """
        print(f"💰 正在获取 {symbol} 的财务数据...")
        
        try:
            stock = yf.Ticker(symbol)
            
            # 获取公司信息
            info = stock.info
            
            # 提取关键财务指标
            financial_data = {
                'symbol': symbol,
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_book': info.get('priceToBook', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'roe': info.get('returnOnEquity', 0),
                'profit_margin': info.get('profitMargins', 0),
                'operating_margin': info.get('operatingMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 1.0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
            }
            
            print(f"✅ 成功获取财务数据")
            return financial_data
            
        except Exception as e:
            print(f"❌ 获取财务数据失败: {str(e)}")
            return {'symbol': symbol}
    
    def collect_news_data(self, symbol: str, days: int = 7) -> List[Dict]:
        """
        收集新闻数据（模拟版本）
        
        Args:
            symbol: 股票代码
            days: 获取最近几天的新闻
            
        Returns:
            新闻列表
        """
        print(f"📰 正在获取 {symbol} 的新闻数据...")
        
        # 注意：这里使用模拟数据，实际应用中可以使用News API
        # 如果有News API key，可以取消下面的注释并使用真实API
        
        """
        # 使用News API的示例代码
        if config.NEWS_API_KEY and config.NEWS_API_KEY != "your-news-api-key":
            try:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': f'{symbol} OR {stock_name}',
                    'apiKey': config.NEWS_API_KEY,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': 10
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    return [{'title': a['title'], 'description': a['description'], 
                            'published_at': a['publishedAt']} for a in articles]
            except Exception as e:
                print(f"News API error: {e}")
        """
        
        # 模拟新闻数据
        simulated_news = [
            {
                'title': f'{symbol} reports strong quarterly earnings',
                'description': 'The company exceeded analyst expectations with robust growth.',
                'sentiment': 'positive',
                'published_at': datetime.now().isoformat()
            },
            {
                'title': f'Market volatility affects {symbol} stock',
                'description': 'Recent market conditions have created uncertainty.',
                'sentiment': 'neutral',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat()
            },
            {
                'title': f'{symbol} announces new product line',
                'description': 'Innovation drives future growth prospects.',
                'sentiment': 'positive',
                'published_at': (datetime.now() - timedelta(days=2)).isoformat()
            }
        ]
        
        print(f"✅ 获取了 {len(simulated_news)} 条新闻")
        return simulated_news
    
    def collect_sentiment_data(self, symbol: str) -> Dict:
        """
        收集社交媒体情绪数据（模拟版本）
        
        Args:
            symbol: 股票代码
            
        Returns:
            情绪数据字典
        """
        print(f"💬 正在获取 {symbol} 的情绪数据...")
        
        # 实际应用中可以使用Reddit API, Twitter API等
        # 这里使用模拟数据
        
        # 模拟情绪得分 (0-1之间，0.5为中性)
        np.random.seed(hash(symbol) % 1000)
        sentiment_score = np.random.beta(5, 5)  # Beta分布，中心在0.5
        
        sentiment_data = {
            'symbol': symbol,
            'sentiment_score': sentiment_score,
            'sentiment_label': self._get_sentiment_label(sentiment_score),
            'positive_mentions': int(np.random.randint(50, 200)),
            'negative_mentions': int(np.random.randint(20, 100)),
            'neutral_mentions': int(np.random.randint(100, 300)),
            'total_mentions': 0,
            'trending_score': np.random.uniform(0, 1),
            'timestamp': datetime.now().isoformat()
        }
        
        sentiment_data['total_mentions'] = (
            sentiment_data['positive_mentions'] + 
            sentiment_data['negative_mentions'] + 
            sentiment_data['neutral_mentions']
        )
        
        print(f"✅ 情绪得分: {sentiment_score:.2f} ({sentiment_data['sentiment_label']})")
        return sentiment_data
    
    @staticmethod
    def _get_sentiment_label(score: float) -> str:
        """将情绪分数转换为标签"""
        if score > 0.6:
            return 'bullish'
        elif score < 0.4:
            return 'bearish'
        else:
            return 'neutral'
    
    def collect_all_data(self, symbol: str, start_date: str, end_date: str) -> Dict:
        """
        收集所有类型的数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            包含所有数据的字典
        """
        print(f"\n{'='*60}")
        print(f"开始收集 {symbol} 的完整数据集")
        print(f"{'='*60}\n")
        
        all_data = {
            'symbol': symbol,
            'price_data': self.collect_stock_data(symbol, start_date, end_date),
            'financial_data': self.collect_financial_data(symbol),
            'news_data': self.collect_news_data(symbol),
            'sentiment_data': self.collect_sentiment_data(symbol),
        }
        
        print(f"\n{'='*60}")
        print(f"✅ {symbol} 数据收集完成!")
        print(f"{'='*60}\n")
        
        return all_data

# 示例使用
if __name__ == "__main__":
    collector = DataCollector(['AAPL'])
    data = collector.collect_all_data('AAPL', '2023-01-01', '2024-01-01')
    print("\n价格数据样本:")
    print(data['price_data'].head())
    print("\n财务数据:")
    print(data['financial_data'])