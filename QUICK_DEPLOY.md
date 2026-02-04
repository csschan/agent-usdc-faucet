# ⚡ 5分钟快速部署指南

## 🎯 目标
将Mock版本部署到公网，获得一个可访问的URL

---

## 方法1: Railway（最简单 - 推荐）

### 步骤：

1. **访问 Railway**
   - 打开: https://railway.app/new
   - 用GitHub登录

2. **Deploy from GitHub Repo**
   - 点击 "Deploy from GitHub repo"
   - 选择你的仓库（需要先push到GitHub）

3. **自动部署**
   - Railway自动检测Procfile
   - 自动安装依赖
   - 自动分配URL

4. **获取URL**
   - 部署完成后，点击项目
   - 在Settings -> Domains找到URL
   - 例如: `https://agent-faucet-production.up.railway.app`

**总时间: 3-5分钟**

---

## 方法2: 无需GitHub - 直接从本地部署

### Railway CLI方式：

```bash
# 1. 安装Railway CLI
npm install -g @railway/cli

# 或使用brew (Mac)
brew install railway

# 2. 登录
railway login

# 3. 初始化项目
railway init

# 4. 部署
railway up

# 5. 打开应用
railway open
```

**总时间: 5分钟**

---

## 方法3: 手动GitHub + Railway

### 如果还没有GitHub仓库：

```bash
# 1. 在GitHub创建新仓库
# 访问: https://github.com/new
# 名称: agent-usdc-faucet
# 描述: Agent-First USDC Testnet Faucet for #USDCHackathon

# 2. 推送代码
cd agent-usdc-faucet
git remote add origin https://github.com/YOUR_USERNAME/agent-usdc-faucet.git
git branch -M main
git push -u origin main

# 3. 在Railway连接GitHub仓库部署
```

---

## 验证部署成功

部署完成后，访问你的URL测试：

```bash
# 替换为你的URL
YOUR_URL="https://your-app.railway.app"

# 测试健康检查
curl $YOUR_URL/health

# 应该返回:
# {"status": "healthy", "mode": "mock", "faucet_balance": 10000.0}
```

---

## 部署后立即做的事

1. **✅ 获取URL并记录**
   - 例如: `https://agent-faucet-production.up.railway.app`

2. **✅ 在Moltbook发布更新**
   - 更新hackathon项目帖子
   - 添加实际可用的API端点

3. **✅ 测试API**
   ```bash
   curl -X POST YOUR_URL/request \
     -H "Content-Type: application/json" \
     -d '{"agent_name": "TestAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Testing"}'
   ```

---

## 当前准备状态

✅ 代码完成
✅ Git仓库初始化
✅ 部署配置文件就绪
✅ Mock模式测试通过

**下一步: 选择一个部署方法并执行**

---

## 需要帮助？

如果你希望我帮你：
- 推送到GitHub
- 或使用Railway CLI部署

请告诉我，我可以生成具体的命令。
