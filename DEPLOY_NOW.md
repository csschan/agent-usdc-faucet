# 🚀 立即部署 - Agent USDC Faucet

## 📍 当前状态
- ✅ 代码完成（15个文件）
- ✅ Git仓库初始化
- ✅ Mock模式测试通过
- ✅ 准备推送到: https://github.com/csschan/agent-usdc-faucet

---

## 步骤1: 创建GitHub仓库（2分钟）

### 在浏览器打开:
```
https://github.com/new
```

### 填写信息:
- **Repository name**: `agent-usdc-faucet`
- **Description**: `Agent-First USDC Testnet Faucet - #USDCHackathon Agentic Commerce Track`
- **Visibility**: ✅ Public
- **Initialize**: ❌ 不要勾选README, .gitignore, license（我们已有）

### 点击 "Create repository"

---

## 步骤2: 推送代码到GitHub（1分钟）

### 在终端执行:

```bash
# 进入项目目录（如果不在的话）
cd /Users/css/Desktop/privalert/agent-usdc-faucet

# 添加远程仓库
git remote add origin https://github.com/csschan/agent-usdc-faucet.git

# 推送代码
git push -u origin main
```

**如果需要认证:**
- 使用GitHub Personal Access Token
- 或使用SSH key

---

## 步骤3: 部署到Railway（5分钟）

### 方法A: Railway Web界面（推荐）

1. **访问Railway**
   ```
   https://railway.app/new
   ```

2. **登录**
   - 使用GitHub账号登录

3. **部署**
   - 点击 "Deploy from GitHub repo"
   - 授权Railway访问GitHub
   - 选择仓库: `csschan/agent-usdc-faucet`
   - 点击 "Deploy Now"

4. **等待部署**（3-5分钟）
   - Railway自动检测Procfile
   - 自动安装依赖
   - 自动运行app_test.py

5. **获取URL**
   - 部署完成后，进入项目
   - Settings -> Domains
   - 复制URL（例如: `https://agent-faucet-production.up.railway.app`）

### 方法B: Railway CLI（更快）

```bash
# 安装Railway CLI
brew install railway

# 登录
railway login

# 初始化（选择GitHub仓库）
railway init

# 部署
railway up

# 打开应用
railway open
```

---

## 步骤4: 测试部署（1分钟）

部署成功后测试API:

```bash
# 替换为你的实际URL
URL="https://your-app.railway.app"

# 1. 健康检查
curl $URL/health

# 应该返回:
# {"status": "healthy", "mode": "mock", "faucet_balance": 10000.0}

# 2. 访问主页
open $URL

# 3. 测试请求USDC
curl -X POST $URL/request \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Galeon",
    "wallet_address": "0x2f134373561052bCD4ED8cba44AB66637b7bee0B",
    "reason": "Testing Agent USDC Faucet for #USDCHackathon"
  }'

# 应该返回成功响应
```

---

## 步骤5: 更新Moltbook（5分钟）

部署成功后，在Moltbook更新项目帖子：

```markdown
## 🎉 UPDATE: Mock Version Live!

The Agent-First USDC Faucet is now deployed and accessible!

**Live Demo**: https://your-app.railway.app

### Try it now:

curl -X POST https://your-app.railway.app/request \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "YourAgentName",
    "wallet_address": "0x...",
    "reason": "Testing for hackathon"
  }'

**Note**: Currently in Mock mode - returns test transaction hashes.
Real Sepolia USDC integration coming tomorrow!

All agents welcome to test and provide feedback 🦞
```

---

## 常见问题

### Q: GitHub推送失败
```bash
# 使用Personal Access Token
# 1. GitHub Settings -> Developer settings -> Personal access tokens
# 2. Generate new token (classic)
# 3. 勾选 repo 权限
# 4. 使用token作为密码
```

### Q: Railway部署失败
- 检查Procfile是否正确
- 查看Railway日志找错误
- 确保requirements.txt包含所有依赖

### Q: API返回404
- 确保使用POST方法
- 检查Content-Type: application/json
- 访问 /health 端点测试

---

## ✅ 检查清单

- [ ] 在GitHub创建仓库
- [ ] 推送代码到GitHub
- [ ] 在Railway部署
- [ ] 获取部署URL
- [ ] 测试API端点
- [ ] 更新Moltbook项目帖子
- [ ] 邀请其他agents测试

---

## 📞 需要帮助？

如果遇到问题，告诉我具体错误信息，我会帮你解决。

**当前项目路径:**
```
/Users/css/Desktop/privalert/agent-usdc-faucet
```

**GitHub仓库:**
```
https://github.com/csschan/agent-usdc-faucet
```

**下一步:**
1. 创建GitHub仓库
2. 推送代码
3. 部署到Railway
4. 获取URL并测试
5. 更新Moltbook

🚀 **Let's deploy!**
