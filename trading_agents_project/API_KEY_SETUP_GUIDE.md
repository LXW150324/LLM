# OpenAI API密钥设置指南

## ⚠️ 重要说明

由于GitHub的安全保护，我们不能将API密钥直接提交到代码库中。请按照以下步骤设置你的API密钥。

## 🔑 方法1: 使用环境变量（推荐）

### Linux/Mac:

1. **创建 .env 文件**:
```bash
cd trading_agents_project
cp .env.example .env
```

2. **编辑 .env 文件**:
```bash
nano .env  # 或使用你喜欢的编辑器
```

3. **填入你的API密钥**:
```
OPENAI_API_KEY=sk-proj-你的API密钥
```

4. **.env 文件会被自动加载**（已在 .gitignore 中，不会被提交）

### Windows:

1. **创建 .env 文件**:
```cmd
cd trading_agents_project
copy .env.example .env
```

2. **用记事本编辑 .env**:
```cmd
notepad .env
```

3. **填入你的API密钥**:
```
OPENAI_API_KEY=sk-proj-你的API密钥
```

## 🔑 方法2: 直接修改配置文件（不推荐）

**注意**: 此方法会将密钥暴露在代码中，不要推送到GitHub！

编辑 `config/config.py` 第28行:
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-proj-你的API密钥")
```

⚠️ **使用此方法后，请不要运行 git push！**

## 🔑 方法3: 系统环境变量

### Linux/Mac:

在 `~/.bashrc` 或 `~/.zshrc` 中添加:
```bash
export OPENAI_API_KEY="sk-proj-你的API密钥"
```

然后重新加载:
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

### Windows:

1. 右键"此电脑" -> "属性"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"用户变量"中点击"新建"
5. 变量名: `OPENAI_API_KEY`
6. 变量值: `sk-proj-你的API密钥`

## 📝 获取API密钥的步骤

### 1. 登录OpenAI账户
访问: https://platform.openai.com/

### 2. 检查账户余额
- 进入: https://platform.openai.com/account/billing
- 确认有可用的credits
- **如果余额为$0，需要充值！**

### 3. 充值账户（如果需要）
- 点击 "Add to credit balance"
- 最低充值: **$5**
- 推荐充值: **$10-20**
- 我们的实验只需: **$0.40**

### 4. 创建API密钥
1. 访问: https://platform.openai.com/api-keys
2. 点击 "Create new secret key"
3. 命名（例如："Trading Agents Experiment"）
4. **立即复制密钥**（只显示一次！）

### 5. 测试密钥
```bash
cd trading_agents_project
python test_api_key.py
```

如果看到 ✅ 成功消息，说明密钥有效！

## 🚀 运行实验

一旦API密钥配置成功：

```bash
# 测试密钥
python test_api_key.py

# 运行真实实验
python run_real_llm_experiment.py

# 或运行演示版本（不需要API密钥）
python run_demo_llm_experiment.py
```

## ❌ 常见错误

### Error: "Access denied"

**原因**:
- OpenAI账户余额为$0
- API密钥权限不足
- API密钥已过期

**解决方案**:
1. 访问 https://platform.openai.com/account/billing
2. 充值账户（最低$5）
3. 等待1-2分钟让系统更新
4. 重新测试

### Error: "Rate limit exceeded"

**原因**: API调用频率过高

**解决方案**:
- 等待1分钟后重试
- 脚本中已有自动重试机制

### Error: "Invalid API key"

**原因**: API密钥格式错误或已撤销

**解决方案**:
1. 检查密钥是否完整复制
2. 创建新的API密钥
3. 更新配置

## 💰 成本控制

### 实验成本
- **GPT-3.5-turbo**: $0.20-0.40（推荐）
- **GPT-4**: $4-7

### 如何选择模型

编辑 `run_real_llm_experiment.py` 第201行:
```python
# 使用GPT-3.5-turbo（便宜）
model="gpt-3.5-turbo",

# 或使用GPT-4（更好但昂贵）
model="gpt-4",
```

## 🔒 安全最佳实践

1. ✅ **使用 .env 文件**（已在 .gitignore）
2. ✅ **不要将密钥提交到git**
3. ✅ **定期轮换API密钥**
4. ✅ **为不同项目使用不同的密钥**
5. ✅ **设置使用限额**（在OpenAI控制台）

## 📞 需要帮助？

如果遇到问题：
- OpenAI文档: https://platform.openai.com/docs/
- OpenAI支持: https://help.openai.com/
- 查看详细错误: `python test_api_detailed.py`

## ✅ 检查清单

在运行实验前，确保：
- [ ] 已获取OpenAI API密钥
- [ ] OpenAI账户有足够的credits（至少$1）
- [ ] API密钥已正确配置（环境变量或配置文件）
- [ ] 运行 `python test_api_key.py` 测试成功
- [ ] 已选择合适的模型（推荐 gpt-3.5-turbo）

完成这些步骤后，你就可以运行真实的LLM实验了！🎉
