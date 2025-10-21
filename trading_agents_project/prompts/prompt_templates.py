"""
Prompt模板管理
存储不同版本的Prompt设计方案
"""

from typing import Dict

class PromptTemplates:
    """Prompt模板集合"""
    
    @staticmethod
    def get_original_prompt() -> str:
        """
        原始TradingAgents的通用Prompt（Baseline 1）
        所有Agent使用相同的通用提示
        """
        return """你是一位专业的金融分析师。请分析提供的数据并给出你对股票的判断。

请基于数据进行分析，并给出你的观点（看多/看空/中性）以及理由。

输出格式要求：
{
    "stance": "bullish/bearish/neutral",
    "reasoning": "你的分析理由"
}
"""
    
    @staticmethod
    def get_simple_template_prompt(role: str) -> str:
        """
        简单模板Prompt（Baseline 3）
        只有角色名称不同，但没有详细的角色定制
        """
        return f"""你是一名{role}，请根据以下信息给出分析。

请给出你的专业判断，并说明理由。

输出格式要求：
{{
    "agent": "{role}",
    "stance": "bullish/bearish/neutral",
    "reasoning": "你的分析理由"
}}
"""
    
    @staticmethod
    def get_random_prompt() -> str:
        """
        随机/不相关Prompt（Baseline 2）
        用于验证Prompt设计的重要性
        """
        import random
        
        random_prompts = [
            "请以诗歌的形式描述你看到的数据。",
            "如果你是一位艺术家，你会如何解读这些信息？",
            "请用隐喻的方式表达你的观点。",
            "假设你在跟朋友聊天，随意说说你的想法。",
            "请简短回答，不超过一句话。"
        ]
        
        return random.choice(random_prompts)
    
    @staticmethod
    def get_role_based_prompts() -> Dict[str, str]:
        """
        基于角色定制的Prompt（我们的方法）
        为每个Agent提供专门设计的提示词
        
        这些已经在各个Agent类中实现，这里提供一个集中的引用
        """
        return {
            'fundamental': """你是一位资深的基本面分析师...""",
            'technical': """你是一位经验丰富的技术分析师...""",
            'sentiment': """你是一位专业的市场情绪分析师...""",
            'news': """你是一位资深的财经新闻分析师...""",
            'bull': """你是一位看多倾向的研究员...""",
            'bear': """你是一位看空倾向的研究员...""",
            'risk': """你是一位专业的风险管理专家...""",
            'trader': """你是一位经验丰富的交易员..."""
        }

class PromptBuilder:
    """动态构建Prompt的工具类"""
    
    @staticmethod
    def build_context_prompt(
        role: str,
        data_description: str,
        task_description: str,
        output_format: str
    ) -> str:
        """
        构建包含上下文的Prompt
        
        Args:
            role: 角色描述
            data_description: 数据说明
            task_description: 任务描述
            output_format: 输出格式要求
            
        Returns:
            完整的Prompt字符串
        """
        prompt = f"""【角色定位】
{role}

【数据说明】
{data_description}

【任务要求】
{task_description}

【输出格式】
{output_format}

请严格按照上述要求完成分析任务。
"""
        return prompt
    
    @staticmethod
    def add_examples(base_prompt: str, examples: list) -> str:
        """
        在Prompt中添加示例（Few-shot learning）
        
        Args:
            base_prompt: 基础Prompt
            examples: 示例列表
            
        Returns:
            添加了示例的Prompt
        """
        examples_text = "\n\n【分析示例】\n"
        
        for i, example in enumerate(examples, 1):
            examples_text += f"\n示例{i}:\n"
            examples_text += f"输入: {example.get('input', '')}\n"
            examples_text += f"输出: {example.get('output', '')}\n"
        
        return base_prompt + examples_text
    
    @staticmethod
    def add_constraints(base_prompt: str, constraints: list) -> str:
        """
        添加约束条件
        
        Args:
            base_prompt: 基础Prompt
            constraints: 约束条件列表
            
        Returns:
            添加了约束的Prompt
        """
        constraints_text = "\n\n【重要约束】\n"
        
        for constraint in constraints:
            constraints_text += f"- {constraint}\n"
        
        return base_prompt + constraints_text