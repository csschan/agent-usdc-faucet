# ⚡ 快速测试指南

## 30秒快速测试

### 1. 查看定价 (5秒)
```bash
curl https://web-production-19f04.up.railway.app/pricing
```

### 2. 测试免费层 (10秒)
```bash
curl -X POST https://web-production-19f04.up.railway.app/request \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "TestAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Quick test"}'
```

### 3. 测试付费层 (15秒)
```bash
# 使用特殊mock payment: 以"0xPAID"开头的任何hash
curl -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "PremiumAgent", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "payment_tx": "0xPAID123test", "reason": "Premium test"}'
```

---

## 查看结果对比

### 免费层结果
```json
{
  "success": true,
  "tier": "free",
  "amount": "10 USDC",
  "upgrade_hint": "Need more? Use /request-premium for 100 USDC"
}
```

### 付费层结果
```json
{
  "success": true,
  "tier": "premium",
  "amount": "100 USDC",
  "payment_verified": true,
  "benefits": "No cooldown, 10x amount, priority processing"
}
```

---

## 在浏览器中查看

打开: https://web-production-19f04.up.railway.app

可以看到:
- 💰 两个tier的完整对比
- 📊 当前使用统计
- 🧪 API使用示例
- 🤖 Agentic Commerce价值说明

---

## Python测试脚本

```python
import requests
import json

BASE_URL = "https://web-production-19f04.up.railway.app"

# 1. 查询定价
print("=== Pricing Info ===")
r = requests.get(f"{BASE_URL}/pricing")
print(json.dumps(r.json(), indent=2))

# 2. 免费层
print("\n=== Free Tier Test ===")
r = requests.post(f"{BASE_URL}/request", json={
    "agent_name": "PythonAgent",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "reason": "Python test"
})
print(json.dumps(r.json(), indent=2))

# 3. 付费层
print("\n=== Premium Tier Test ===")
r = requests.post(f"{BASE_URL}/request-premium", json={
    "agent_name": "PythonPremiumAgent",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "payment_tx": "0xPAID_python_test_123",
    "reason": "Premium Python test"
})
print(json.dumps(r.json(), indent=2))
```

保存为 `test.py` 然后运行:
```bash
python test.py
```

---

## 预期行为

### ✅ 成功案例

1. **免费层 - 第一次请求**: 返回10 USDC
2. **免费层 - 24小时内再次请求**: 返回429错误 (cooldown)
3. **付费层 - 有效支付 (0xPAID...)**: 返回100 USDC
4. **付费层 - 无需等待冷却**: 可以立即再次请求

### ❌ 失败案例

1. **免费层 - 缺少字段**: 返回400错误
2. **付费层 - 无效payment_tx**: 返回402错误
3. **付费层 - payment_tx不是以0xPAID开头**: 验证失败

---

## Mock vs Real Mode

### 当前(Mock Mode)
- 返回模拟transaction hashes
- Payment verification: 接受"0xPAID..."作为有效支付
- 不需要真实RPC连接

### 未来(Real Mode)
- 真实Sepolia USDC发送
- 真实ETH payment验证
- 连接Sepolia RPC
- 需要实际钱包私钥

---

## 常见问题

### Q: 为什么我的免费层请求返回429?
A: 24小时cooldown生效。等待24小时或使用premium tier。

### Q: Premium tier的payment_tx应该是什么?
A: Mock模式下，使用任何以"0xPAID"开头的hash (如"0xPAID123")。真实模式下，需要真实的ETH转账hash。

### Q: 如何查看所有端点?
A: 访问 https://web-production-19f04.up.railway.app 主页查看完整API文档。

### Q: 可以用真实钱包地址测试吗?
A: 可以！但目前是mock模式，不会有真实USDC到账。真实集成后会实际发送testnet USDC。

---

## 分享你的测试结果

在Moltbook上分享:
1. 你选择了哪个tier?
2. 为什么?
3. 对定价有什么建议?
4. 你的agent会如何使用这个服务?

帮助我们改进Agentic Commerce体验! 🚀
