"""
详细测试OpenAI API密钥，显示完整错误信息
"""

from openai import OpenAI
from config.config import config
import traceback

def test_api_detailed():
    """详细测试API密钥"""
    print("="*70)
    print("详细测试OpenAI API密钥")
    print("="*70)

    api_key = config.OPENAI_API_KEY
    print(f"\nAPI密钥: {api_key[:25]}...{api_key[-15:]}")
    print(f"密钥长度: {len(api_key)}")

    try:
        client = OpenAI(api_key=api_key)
        print("\n✅ OpenAI客户端初始化成功")

        print("\n尝试1: 使用 gpt-3.5-turbo...")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Say 'Hello'"}
                ],
                max_tokens=10
            )
            print(f"✅ 成功！响应: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            print(f"\n完整错误信息:")
            traceback.print_exc()

        print("\n尝试2: 使用 gpt-4o-mini (更新的模型)...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": "Say 'Hello'"}
                ],
                max_tokens=10
            )
            print(f"✅ 成功！响应: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")

        # 尝试列出可用模型
        print("\n尝试3: 获取账户模型列表...")
        try:
            models = client.models.list()
            print(f"✅ 成功获取模型列表:")
            for model in list(models)[:5]:
                print(f"  - {model.id}")
            return True
        except Exception as e:
            print(f"❌ 失败: {e}")
            print(f"\n完整错误信息:")
            traceback.print_exc()

        return False

    except Exception as e:
        print(f"\n❌ 客户端初始化失败: {e}")
        print(f"\n完整错误信息:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n这将尝试多种方式测试API密钥\n")
    success = test_api_detailed()

    if not success:
        print("\n" + "="*70)
        print("可能的原因:")
        print("1. API密钥已过期或被撤销")
        print("2. OpenAI账户没有足够的credits（需要充值）")
        print("3. API密钥没有正确的权限")
        print("4. 网络或代理问题")
        print("\n解决方案:")
        print("1. 访问 https://platform.openai.com/account/billing")
        print("   检查账户余额并充值（最低$5）")
        print("2. 访问 https://platform.openai.com/api-keys")
        print("   创建新的API密钥")
        print("3. 确保账户状态正常")
        print("="*70)
