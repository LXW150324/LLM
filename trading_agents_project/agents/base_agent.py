"""
基础Agent类
所有具体Agent的父类，提供LLM调用的基础功能
"""

from openai import OpenAI
import time
import json
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

from config.config import config

class BaseAgent(ABC):
    """Agent基类"""

    def __init__(self, role_name: str, api_key: str = None):
        """
        初始化Agent

        Args:
            role_name: Agent角色名称
            api_key: OpenAI API密钥
        """
        self.role_name = role_name
        self.api_key = api_key or config.OPENAI_API_KEY

        # 初始化OpenAI客户端（新版API）
        self.client = OpenAI(api_key=self.api_key)

        # 设置LLM参数
        self.model = config.OPENAI_MODEL
        self.temperature = config.AGENT_TEMPERATURE
        self.max_tokens = config.OPENAI_MAX_TOKENS
        self.max_retries = config.MAX_RETRIES

        # 对话历史
        self.conversation_history = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        获取系统提示词（每个具体Agent需要实现）
        
        Returns:
            系统提示词字符串
        """
        pass
    
    @abstractmethod
    def format_input_data(self, data: Dict) -> str:
        """
        格式化输入数据（每个具体Agent需要实现）
        
        Args:
            data: 输入数据字典
            
        Returns:
            格式化后的输入字符串
        """
        pass
    
    def call_llm(self, user_message: str, system_prompt: str = None) -> str:
        """
        调用LLM获取响应
        
        Args:
            user_message: 用户消息
            system_prompt: 系统提示词（如果为None则使用默认的）
            
        Returns:
            LLM的响应文本
        """
        if system_prompt is None:
            system_prompt = self.get_system_prompt()
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # 添加对话历史（如果有）
        if self.conversation_history:
            messages = [messages[0]] + self.conversation_history + [messages[1]]
        
        for attempt in range(self.max_retries):
            try:
                # 使用新版OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )

                assistant_message = response.choices[0].message.content

                # 保存到对话历史
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})

                return assistant_message

            except Exception as e:
                error_str = str(e)

                # 处理速率限制错误
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    wait_time = (attempt + 1) * 5
                    print(f"⏳ API速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

                # 处理其他API错误
                elif "api" in error_str.lower():
                    print(f"❌ API错误: {error_str}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2)
                    else:
                        raise

                # 处理其他异常
                else:
                    print(f"❌ 调用LLM时出错: {error_str}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2)
                    else:
                        raise

        raise Exception(f"调用LLM失败，已重试 {self.max_retries} 次")
    
    def analyze(self, data: Dict) -> Dict:
        """
        分析数据并返回结果
        
        Args:
            data: 输入数据
            
        Returns:
            分析结果字典
        """
        # 格式化输入
        formatted_input = self.format_input_data(data)
        
        # 调用LLM
        response = self.call_llm(formatted_input)
        
        # 解析响应
        result = self.parse_response(response)
        
        return result
    
    def parse_response(self, response: str) -> Dict:
        """
        解析LLM响应为结构化数据
        
        Args:
            response: LLM响应文本
            
        Returns:
            解析后的结果字典
        """
        # 尝试提取JSON
        try:
            # 查找JSON块
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                return result
        except:
            pass
        
        # 如果无法提取JSON，返回原始文本
        return {
            'agent': self.role_name,
            'raw_response': response,
            'stance': self._extract_stance(response),
            'confidence': self._extract_confidence(response)
        }
    
    def _extract_stance(self, text: str) -> str:
        """从文本中提取立场"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['bullish', 'buy', 'positive', 'upward', '看涨', '买入']):
            return 'bullish'
        elif any(word in text_lower for word in ['bearish', 'sell', 'negative', 'downward', '看跌', '卖出']):
            return 'bearish'
        else:
            return 'neutral'
    
    def _extract_confidence(self, text: str) -> float:
        """从文本中提取信心度"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['very confident', 'highly confident', 'strong', '非常确信']):
            return 0.9
        elif any(word in text_lower for word in ['confident', 'likely', '确信', '可能']):
            return 0.7
        elif any(word in text_lower for word in ['moderate', 'possible', '中等', '也许']):
            return 0.5
        elif any(word in text_lower for word in ['low confidence', 'uncertain', '不确定']):
            return 0.3
        else:
            return 0.5
    
    def clear_history(self):
        """清除对话历史"""
        self.conversation_history = []
    
    def __repr__(self):
        return f"{self.__class__.__name__}(role={self.role_name})"