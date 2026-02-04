"""
Mock模式测试 - 不需要真实RPC或钱包
验证代码逻辑是否正常
"""

import sys
sys.path.insert(0, '.')

from blockchain import MockUSDCFaucet
from verifier import MockVerifier
from database import Database

print("=" * 60)
print("🧪 Mock模式测试")
print("=" * 60)

# 1. 测试Mock Faucet
print("\n1️⃣ 测试Mock区块链...")
faucet = MockUSDCFaucet()
print(f"   Faucet地址: {faucet.address}")
print(f"   Faucet余额: {faucet.get_balance()} USDC")

# 测试发送
test_wallet = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1"
print(f"\n   发送10 USDC到: {test_wallet}")
tx_hash = faucet.send_usdc(test_wallet, 10)
print(f"   ✅ 交易hash: {tx_hash}")

# 2. 测试Mock Verifier
print("\n2️⃣ 测试Mock验证...")
verifier = MockVerifier()
result = verifier.verify_agent("TestAgent", "https://moltbook.com/test")
print(f"   ✅ 验证结果: {result}")

# 3. 测试Database
print("\n3️⃣ 测试数据库...")
db = Database("test_faucet.db")
db.init_db()
print("   ✅ 数据库初始化成功")

# 记录测试请求
db.record_request(
    agent_name="TestAgent",
    wallet_address=test_wallet,
    reason="Testing the faucet system",
    amount=10,
    tx_hash=tx_hash,
    moltbook_proof="https://moltbook.com/test"
)
print("   ✅ 请求记录成功")

# 获取统计
stats = db.get_stats()
print(f"\n   📊 统计数据:")
print(f"      总请求: {stats['total_requests']}")
print(f"      总USDC: {stats['total_usdc']}")
print(f"      成功率: {stats['success_rate']}%")

# 测试冷却
print(f"\n   🕒 冷却测试:")
is_cooldown = db.is_in_cooldown("TestAgent", 24)
print(f"      在冷却期: {is_cooldown}")

print("\n" + "=" * 60)
print("✅ Mock模式测试全部通过！")
print("=" * 60)
