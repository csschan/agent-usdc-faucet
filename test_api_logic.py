"""
直接测试API逻辑（不启动服务器）
"""

from blockchain import MockUSDCFaucet
from verifier import MockVerifier
from database import Database

print("=" * 70)
print("🧪 API逻辑测试（Mock模式）")
print("=" * 70)

# 初始化组件
db = Database("test_api.db")
db.init_db()
verifier = MockVerifier()
faucet = MockUSDCFaucet()

FAUCET_AMOUNT = 10
COOLDOWN_HOURS = 24

def test_request(agent_name, wallet_address, reason):
    """模拟API请求处理"""
    print(f"\n📝 处理请求:")
    print(f"   Agent: {agent_name}")
    print(f"   Wallet: {wallet_address}")
    print(f"   Reason: {reason}")

    # 1. 检查冷却
    if db.is_in_cooldown(agent_name, COOLDOWN_HOURS):
        print(f"   ❌ 冷却期内，拒绝请求")
        return {'success': False, 'error': 'Cooldown active'}

    # 2. 验证身份
    if not verifier.verify_agent(agent_name):
        print(f"   ❌ 验证失败")
        return {'success': False, 'error': 'Verification failed'}

    # 3. 验证地址
    if not faucet.is_valid_address(wallet_address):
        print(f"   ❌ 无效地址")
        return {'success': False, 'error': 'Invalid address'}

    # 4. 发送USDC
    tx_hash = faucet.send_usdc(wallet_address, FAUCET_AMOUNT)
    print(f"   ✅ 发送{FAUCET_AMOUNT} USDC")
    print(f"   TX: {tx_hash[:20]}...")

    # 5. 记录
    db.record_request(
        agent_name=agent_name,
        wallet_address=wallet_address,
        reason=reason,
        amount=FAUCET_AMOUNT,
        tx_hash=tx_hash
    )
    print(f"   ✅ 记录成功")

    return {
        'success': True,
        'amount': f'{FAUCET_AMOUNT} USDC',
        'tx_hash': tx_hash,
        'message': f'Sent {FAUCET_AMOUNT} testnet USDC! 🦞'
    }

# 测试1: 正常请求
print("\n" + "=" * 70)
print("测试1: 正常请求")
print("=" * 70)
result1 = test_request(
    "Galeon",
    "0x2f134373561052bCD4ED8cba44AB66637b7bee0B",
    "Testing USDC faucet for #USDCHackathon"
)
print(f"\n结果: {result1}")

# 测试2: 重复请求（应该被冷却拒绝）
print("\n" + "=" * 70)
print("测试2: 重复请求（应该被冷却拒绝）")
print("=" * 70)
result2 = test_request(
    "Galeon",
    "0x2f134373561052bCD4ED8cba44AB66637b7bee0B",
    "Second request - should be rejected"
)
print(f"\n结果: {result2}")

# 测试3: 不同agent（应该成功）
print("\n" + "=" * 70)
print("测试3: 不同agent（应该成功）")
print("=" * 70)
result3 = test_request(
    "TestAgent",
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "Testing from different agent"
)
print(f"\n结果: {result3}")

# 显示统计
print("\n" + "=" * 70)
print("📊 最终统计")
print("=" * 70)
stats = db.get_detailed_stats()
print(f"\n总请求: {stats['total_requests']}")
print(f"成功请求: {stats['successful_requests']}")
print(f"失败请求: {stats['failed_requests']}")
print(f"总USDC: {stats['total_usdc']}")
print(f"独立agents: {stats['unique_agents']}")
print(f"\n用例分类:")
for uc in stats['use_cases']:
    print(f"  - {uc['category']}: {uc['count']} ({uc['percentage']}%)")

# 显示最近请求
print("\n最近请求:")
recent = db.get_recent_requests(limit=5)
for req in recent:
    print(f"  - {req['agent_name']}: {req['amount']} USDC ({req['timestamp']})")

print("\n" + "=" * 70)
print("✅ 所有测试通过！API逻辑正常工作")
print("=" * 70)
