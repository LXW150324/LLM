"""
测试OpenAI API密钥是否有效
"""

from openai import OpenAI
from config.config import config

def test_api_key():
    """测试API密钥"""
    print("="*70)
    print("测试OpenAI API密钥")
    print("="*70)

    api_key = config.OPENAI_API_KEY
    print(f"\nAPI密钥: {api_key[:20]}...{api_key[-10:]}")

    try:
        client = OpenAI(api_key=api_key)
        print("\n✅ OpenAI客户端初始化成功")

        print("\n发送测试请求...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 使用更便宜的模型测试
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API test successful' if you can read this."}
            ],
            max_tokens=50
        )

        content = response.choices[0].message.content
        print(f"\n✅ API调用成功！")
        print(f"GPT响应: {content}")
        print(f"\n使用的模型: {response.model}")
        print(f"Token使用: {response.usage.total_tokens}")

        return True

    except Exception as e:
        print(f"\n❌ API测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n" + "="*70)
        print("✅ API密钥有效！可以运行真实实验了")
        print("运行命令: python run_real_llm_experiment.py")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("❌ API密钥无效，请检查密钥或账户状态")
        print("="*70)
