# 🚀 Deployment Guide - Agent USDC Faucet

## Quick Deploy Options

### Option 1: Railway (推荐 - 最简单)

1. **登录Railway**
   - 访问: https://railway.app/
   - 用GitHub账号登录

2. **部署项目**
   ```bash
   # 在本地项目目录
   railway login
   railway init
   railway up
   ```

3. **获取URL**
   - Railway会自动分配一个URL
   - 例如: `https://agent-faucet.railway.app`

4. **完成！**
   - Mock模式自动运行
   - 无需配置环境变量

---

### Option 2: Render (备选)

1. **创建账号**
   - 访问: https://render.com/
   - 用GitHub账号登录

2. **New Web Service**
   - 连接GitHub仓库
   - 或直接上传代码

3. **配置**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app_test:app`
   - 免费计划即可

4. **部署**
   - 点击Deploy
   - 等待3-5分钟

---

### Option 3: Heroku

1. **安装Heroku CLI**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **登录并创建应用**
   ```bash
   heroku login
   heroku create agent-usdc-faucet
   ```

3. **部署**
   ```bash
   git push heroku main
   ```

4. **打开应用**
   ```bash
   heroku open
   ```

---

## 手动部署（任何VPS）

### 使用Docker

1. **创建Dockerfile**（已包含）

2. **构建并运行**
   ```bash
   docker build -t agent-faucet .
   docker run -p 8080:8080 agent-faucet
   ```

### 直接运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行Mock模式
python app_test.py

# 或使用gunicorn（生产环境）
gunicorn app_test:app --bind 0.0.0.0:8080
```

---

## 环境变量（真实版本需要）

当切换到真实Sepolia版本时，需要配置：

```bash
# Railway / Render 环境变量设置
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
FAUCET_PRIVATE_KEY=your_private_key_here
PORT=8080
```

---

## 验证部署

部署后访问这些端点验证：

```bash
# 替换为你的实际URL
URL="https://your-app.railway.app"

# 1. 健康检查
curl $URL/health

# 2. 主页
open $URL

# 3. 测试请求
curl -X POST $URL/request \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "TestAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Testing"}'
```

---

## 故障排查

### 应用无法启动
- 检查`Procfile`是否正确
- 确认Python版本匹配`runtime.txt`
- 查看平台日志

### 端口错误
- 确保使用`$PORT`环境变量
- Railway/Render会自动分配端口

### 依赖安装失败
- 检查`requirements.txt`
- 确保所有包版本兼容

---

## 推荐部署流程（3天hackathon）

**Day 1 (今天):**
- ✅ 部署Mock版本到Railway
- ✅ 获取公开URL
- ✅ 在Moltbook发布更新

**Day 2 (明天):**
- 获取真实Sepolia资源
- 切换到真实版本
- 重新部署
- 邀请agents测试

**Day 3 (最后一天):**
- 收集使用数据
- 完善文档
- 录制demo视频
- 投票其他项目

---

## 当前状态

**Mock版本已准备好部署！**

运行以下命令查看部署选项：
```bash
# Railway (推荐)
railway login
railway init

# 或手动部署文档
cat DEPLOYMENT.md
```
