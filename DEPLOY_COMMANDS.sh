#!/bin/bash

echo "=========================================="
echo "🚀 部署Agent USDC Faucet到GitHub + Railway"
echo "=========================================="
echo ""

# Step 1: 推送到GitHub
echo "步骤1: 推送到GitHub..."
echo ""
echo "执行以下命令:"
echo ""
cat << 'COMMANDS'
# 添加远程仓库
git remote add origin https://github.com/csschan/agent-usdc-faucet.git

# 重命名分支为main
git branch -M main

# 推送到GitHub
git push -u origin main

COMMANDS

echo ""
echo "=========================================="
echo "步骤2: 在Railway部署"
echo "=========================================="
echo ""
echo "1. 访问: https://railway.app/new"
echo "2. 点击 'Deploy from GitHub repo'"
echo "3. 授权Railway访问GitHub"
echo "4. 选择仓库: csschan/agent-usdc-faucet"
echo "5. 等待自动部署（3-5分钟）"
echo "6. 获取URL并测试"
echo ""
echo "=========================================="
echo "或者使用Railway CLI (更快):"
echo "=========================================="
echo ""
cat << 'CLI'
# 安装Railway CLI
brew install railway

# 登录Railway
railway login

# 链接到GitHub仓库
railway link

# 部署
railway up

# 打开应用
railway open

CLI

echo ""
echo "=========================================="
echo "✅ 准备就绪！选择上面任一方法部署"
echo "=========================================="
