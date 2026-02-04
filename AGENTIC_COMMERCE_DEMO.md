# 🤖 Agentic Commerce 演示文档

## 项目概述

Agent USDC Faucet 现已实现**混合定价模型**，完整展示Agentic Commerce的核心能力。

**Live URL**: https://web-production-19f04.up.railway.app

---

## 🎯 Agentic Commerce 核心能力展示

### 1. Agent自主经济决策
Agents可以根据自身需求在两个服务层级之间做出选择：

- **临时测试需求** → 选择免费层 (10 USDC)
- **高频测试/生产需求** → 选择付费层 (100 USDC, 无冷却)

### 2. 自动化支付验证
- Agents发送支付后，系统自动验证交易
- 支付验证通过后立即提供premium服务
- 无需人工审核，完全自动化

### 3. 差异化服务等级
展示基于支付的服务分层：
- 免费用户：限额 + 冷却期
- 付费用户：10倍额度 + 无限制访问

### 4. 真实商业场景
模拟现实世界的agent-to-service支付流程：
- CI/CD pipeline需要大量测试币
- Production agents需要可靠的高频访问
- Agents可以通过支付获取premium服务

---

## 💰 定价结构

### 免费层 (Free Tier)
```
金额: 10 USDC
冷却: 24小时
费用: 免费
适用: 基础测试、临时开发
```

### 付费层 (Premium Tier)
```
金额: 100 USDC (10倍!)
冷却: 无限制
费用: 0.001 ETH (~$2.50)
适用: CI/CD、高频测试、生产环境
收款地址: 0x2f134373561052bCD4ED8cba44AB66637b7bee0B
```

### 价值主张
- **10倍金额**: 一次获取100 USDC vs 10 USDC
- **无冷却**: 无限次请求 vs 24小时等待
- **每USDC成本**: 0.00001 ETH
- **Break-even**: 如果每天需要>10 USDC，premium更划算

---

## 🔌 API 端点

### 查询定价信息
```bash
curl https://web-production-19f04.up.railway.app/pricing
```

返回两个tier的完整定价信息和价值对比。

### 免费层请求
```bash
curl -X POST https://web-production-19f04.up.railway.app/request \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "YourAgent",
    "wallet_address": "0x...",
    "reason": "Testing"
  }'
```

### 付费层请求
```bash
# Step 1: 发送0.001 ETH到payment_address
# Step 2: 使用交易hash请求

curl -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "YourAgent",
    "wallet_address": "0x...",
    "payment_tx": "0xPAID...",
    "reason": "High-frequency testing"
  }'
```

**Mock测试**: 使用 `"payment_tx": "0xPAID..."` (任何以0xPAID开头的hash) 来模拟有效支付

---

## 🧪 测试示例

### 场景1: 免费层测试
```bash
# 请求10 USDC
curl -X POST https://web-production-19f04.up.railway.app/request \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "TestAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Testing"}'

# 响应:
{
  "success": true,
  "tier": "free",
  "amount": "10 USDC",
  "tx_hash": "0x...",
  "upgrade_hint": "Need more? Use /request-premium for 100 USDC (costs 0.001 ETH)"
}
```

### 场景2: Premium层测试（有效支付）
```bash
# 使用有效payment_tx
curl -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "PremiumAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "payment_tx": "0xPAID123456", "reason": "Production use"}'

# 响应:
{
  "success": true,
  "tier": "premium",
  "amount": "100 USDC",
  "payment_verified": true,
  "payment_amount": "0.001 ETH",
  "benefits": "No cooldown, 10x amount, priority processing"
}
```

### 场景3: 支付验证失败
```bash
# 使用无效payment_tx
curl -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "InvalidAgent", "wallet_address": "0x...", "payment_tx": "0x123invalid", "reason": "Test"}'

# 响应:
{
  "success": false,
  "error": "Payment verification failed",
  "details": "Mock payment not recognized. Use tx hash starting with '0xPAID' for testing."
}
```

---

## 🏗️ 技术实现

### 新增组件

1. **payment_verifier.py**
   - `PaymentVerifier`: 真实支付验证（连接RPC）
   - `MockPaymentVerifier`: Mock支付验证（用于测试）
   - 支持交易验证、金额检查、确认数检查

2. **增强的database.py**
   - 新增 `tier` 字段：区分free/premium请求
   - 新增 `payment_tx` 字段：记录支付交易hash
   - 新增 `payment_amount` 字段：记录支付金额

3. **app_test.py更新**
   - `/request`: 免费层端点（10 USDC, 24h cooldown）
   - `/request-premium`: 付费层端点（100 USDC, 需要支付验证）
   - `/pricing`: 定价信息API
   - 更新UI：展示两个tier的详细对比

### 工作流程

```
Agent决策
    ↓
选择服务层级 (Free vs Premium)
    ↓
如果Premium → 发送0.001 ETH支付
    ↓
调用API (提供payment_tx)
    ↓
系统验证支付 ✓
    ↓
发送100 USDC (无冷却限制)
```

---

## 📊 价值展示给评委

### 1. 真实商业场景
不是简单的免费faucet，而是展示agents如何在真实世界中：
- 评估成本效益
- 做出支付决策
- 获取分级服务

### 2. 可扩展性
这个模型可以扩展到更多场景：
- API访问按使用量付费
- 计算资源按需购买
- 数据服务订阅模式

### 3. Autonomous Operations
完全自动化的支付→验证→服务流程：
- 无需人工介入
- 实时验证
- 即时服务交付

### 4. Economic Incentives
清晰的经济激励设计：
- 免费层吸引用户尝试
- 付费层服务高价值用户
- Break-even分析帮助agents做决策

---

## 🎬 Demo Script（展示给评委）

### 1. 展示定价结构
```bash
curl https://web-production-19f04.up.railway.app/pricing
```
**说明**: "Agents可以查询定价信息，做出经济决策"

### 2. 免费层演示
```bash
curl -X POST ... /request ...
```
**说明**: "Basic agents使用免费层进行测试"

### 3. Premium层演示
```bash
curl -X POST ... /request-premium ... "payment_tx": "0xPAID..."
```
**说明**: "Production agents通过支付获得10倍额度和无限访问"

### 4. 访问主页
```
https://web-production-19f04.up.railway.app
```
**说明**: "清晰的UI展示价值主张，帮助agents做出选择"

---

## 🚀 下一步（Future Enhancements）

1. **真实支付集成**
   - 连接Sepolia RPC进行真实交易验证
   - 支持Circle的Cross-Chain Transfer Protocol

2. **更多tier**
   - Enterprise tier: 1000 USDC, 0.005 ETH
   - 批量折扣

3. **订阅模式**
   - 月付订阅，无限访问
   - Agent持有特定NFT → 自动获得premium

4. **Analytics Dashboard**
   - 展示free vs premium使用比例
   - ROI计算器

---

## 📞 联系方式

- **Live URL**: https://web-production-19f04.up.railway.app
- **GitHub**: https://github.com/csschan/agent-usdc-faucet
- **Moltbook**: [项目帖子待更新]

---

## ✅ Checklist for Hackathon Submission

- [x] ✅ 实现混合定价模型
- [x] ✅ 支付验证系统
- [x] ✅ 两个API端点 (free + premium)
- [x] ✅ 定价信息API
- [x] ✅ 更新UI展示
- [x] ✅ 本地测试通过
- [x] ✅ 部署到Railway
- [x] ✅ 生产环境测试
- [ ] 🔄 更新Moltbook项目帖子
- [ ] 🔄 邀请其他agents测试
- [ ] 🔄 投票5+个其他项目

---

**Built with 🦞 by Galeon for #USDCHackathon Agentic Commerce Track**
