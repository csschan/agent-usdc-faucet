# ⚡ 30-Second Quick Test Guide

**For Judges & Other Agents**: Quickly verify the core functionality of the Agent-First USDC Faucet

**Live URL**: https://web-production-19f04.up.railway.app

---

## 🎯 3 Test Scenarios (Each <10 seconds)

### Scenario 1: Agent Queries Pricing and Makes Decisions (Demonstrating Autonomous Economic Decision-Making)

```bash
# Agent autonomously retrieves pricing information
curl https://web-production-19f04.up.railway.app/pricing
```

**Expected Result**:
```json
{
  "tiers": {
    "free": {
      "amount_usdc": 10,
      "cooldown_hours": 24,
      "cost_eth": 0,
      "endpoint": "/request"
    },
    "premium": {
      "amount_usdc": 100,
      "cooldown_hours": 0,
      "cost_eth": 0.001,
      "payment_address": "0x2f134373561052bCD4ED8cba44AB66637b7bee0B",
      "endpoint": "/request-premium"
    }
  },
  "value_proposition": {
    "premium_multiplier": "10.0x more USDC",
    "cost_per_usdc": "1e-05 ETH per USDC",
    "break_even": "Worth it if you need >10 USDC per day"
  }
}
```

**Why This Matters**:
- Agent can retrieve complete pricing in <100ms
- Automatically calculates ROI and break-even point
- Humans need to open webpage, read, calculate (5-10 minutes)
- **Agent is 60-600x faster than humans**

---

### Scenario 2: Agent Uses Free Tier (Demonstrating Basic Automation)

```bash
# Agent autonomously requests testnet USDC
curl -X POST https://web-production-19f04.up.railway.app/request \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "TestAgent_'$(date +%s)'",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "reason": "Testing Agent-First Faucet for #USDCHackathon"
  }'
```

**Expected Result**:
```json
{
  "success": true,
  "tier": "free",
  "amount": "10 USDC",
  "tx_hash": "0x...",
  "message": "✅ Sent 10 testnet USDC (Free tier)",
  "upgrade_hint": "Need more? Use /request-premium for 100 USDC (costs 0.001 ETH)"
}
```

**Why This Matters**:
- Fully automated, no human approval needed
- Agent can automatically obtain test tokens in CI/CD pipelines
- Available 24/7, not limited by time zones
- **Agent is more reliable than humans** (doesn't forget, doesn't delay)

---

### Scenario 3: Agent Uses Premium Tier (Demonstrating Autonomous Payment Decisions)

#### Method A: Mock Testing (Quick Concept Verification)

```bash
# Mock test: Use "0xPAID" prefix to simulate payment
curl -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "PremiumAgent_'$(date +%s)'",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "payment_tx": "0xPAID_test_'$(date +%s)'",
    "reason": "Mock testing premium tier"
  }'
```

#### Method B: Real Autonomous Payment (Production Environment)

**Fully automated workflow when Agents have Web3 capabilities**:

```python
# Agent operates completely autonomously, no human intervention
from web3 import Web3
from eth_account import Account

# 1. Agent autonomously signs and sends payment
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io'))
account = Account.from_key(agent_private_key)
tx = {
    'to': '0x2f134373561052bCD4ED8cba44AB66637b7bee0B',
    'value': w3.to_wei(0.001, 'ether'),
    'gas': 21000,
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(account.address)
}
signed_tx = account.sign_transaction(tx)
payment_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction).hex()

# 2. Agent autonomously requests service
import requests
requests.post('/request-premium', json={
    'agent_name': 'AutoAgent',
    'wallet_address': account.address,
    'payment_tx': payment_hash  # Automatically obtained real tx hash
})
```

**Key Point**: Agent has private key → Fully autonomous payment → Zero human intervention

**Expected Result**:
```json
{
  "success": true,
  "tier": "premium",
  "amount": "100 USDC",
  "payment_verified": true,
  "payment_amount": "0.001 ETH",
  "benefits": "No cooldown, 10x amount, priority processing",
  "message": "✅ Sent 100 testnet USDC (Premium tier)"
}
```

**Why This Matters**:
- Agent autonomously evaluates needs → Decides whether to pay
- Automatic payment verification, no human review needed
- Instant service delivery, no waiting time
- **Agent is more optimized than humans** (based on algorithms, not guessing)

---

### Scenario 4: Balance System (TRUE AUTONOMOUS Fully Automatic) ⚡

**This is true Agent Commerce**: Deposit once, use multiple times automatically, no per-request transaction signing

#### Step 1: Deposit
```bash
curl -X POST https://web-production-19f04.up.railway.app/deposit \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "AutonomousAgent",
    "amount_eth": 0.01,
    "deposit_tx": "0xDEPOSIT_'$(date +%s)'"
  }'
```

**Expected Result**:
```json
{
  "success": true,
  "deposit_amount": 0.01,
  "new_balance": 0.01,
  "message": "Deposit successful! 0.01 ETH added to balance.",
  "usage": "You can now use /request-premium-balance for autonomous requests"
}
```

#### Step 2: Check Balance
```bash
curl "https://web-production-19f04.up.railway.app/balance?agent_name=AutonomousAgent"
```

**Expected Result**:
```json
{
  "success": true,
  "agent_name": "AutonomousAgent",
  "balance_eth": 0.01,
  "has_balance": true
}
```

#### Step 3: Automatically Use Balance for Premium Service (Repeatable)
```bash
curl -X POST https://web-production-19f04.up.railway.app/request-premium-balance \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "AutonomousAgent",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "reason": "Autonomous CI/CD testing"
  }'
```

**Expected Result**:
```json
{
  "success": true,
  "tier": "premium_balance",
  "amount": "100 USDC",
  "balance_deducted": 0.001,
  "remaining_balance": 0.009,
  "note": "TRUE AUTONOMOUS: No per-request web3 transaction needed!",
  "benefits": "Deposited once, used autonomously - this is true Agentic Commerce"
}
```

#### Use Again (No Transaction Signing Needed)
```bash
# Request immediately again - no new web3 transaction needed!
curl -X POST https://web-production-19f04.up.railway.app/request-premium-balance \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "AutonomousAgent",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "reason": "Second autonomous request"
  }'
```

**Why This is TRUE Agentic Commerce**:
- ✅ **Deposit once, use 10 times**: 0.01 ETH = 10 premium requests
- ✅ **Zero per-request transactions**: No need to sign and broadcast transaction each time
- ✅ **Fully autonomous**: Agent can decide when to use balance on its own
- ✅ **Faster**: Saves transaction delay each time (~15s → <1s)
- ✅ **Cheaper**: Saves 9 gas fees

**Comparison with Humans**:
- Human: Each time must open wallet → Confirm transaction → Wait → Copy hash → Paste → Submit (~2 minutes each)
- Agent: After one deposit, each request takes <100ms, fully automated

**Real Use Case**:
```python
# Production CI/CD Agent
agent.deposit(0.1)  # Deposit once, can use 100 times
for test in tests:
    usdc = agent.request_premium()  # Auto-deducts balance each time, no human needed
    test.run(usdc)
# Fully autonomous, zero human intervention
```

---

## 🤖 Complete Agent Workflow (Real Scenario)

**Scenario**: Production CI/CD agent needs to run 100 tests, each requiring 10 USDC

### Human Method (Slow, Unreliable):
```
1. Open faucet webpage (30 seconds)
2. Fill out form (30 seconds)
3. Wait 24 hours for cooldown
4. Repeat 100 times = 100 days!
5. Or fill out application for bulk USDC = Wait for human approval (days)
```
**Total Time**: Days to months

### Agent Method (Fast, Reliable):
```python
# Agent autonomous decision-making code
pricing = requests.get('https://.../pricing').json()

# Calculate needs
total_need = 100 * 10  # 1000 USDC
free_tier_days = total_need / 10  # 100 days

# Autonomous decision
if free_tier_days > 1:
    # Premium is better
    send_payment(0.001)  # ETH
    request_premium(payment_tx)
    # Immediately get 100 USDC, can request again immediately
    # 10 premium requests = 1000 USDC
else:
    # Free is better
    request_free()
```
**Total Time**: <10 seconds to decide, <1 minute to complete all requests

**Agent is 86,400x+ faster than human** (assuming human needs 1 day, agent needs 1 second)

---

## 📊 System Status Check

### Health Check
```bash
curl https://web-production-19f04.up.railway.app/health
```

Expected: `{"status": "healthy", "mode": "mock", "faucet_balance": 10000.0}`

### Real-time Statistics
```bash
curl https://web-production-19f04.up.railway.app/stats
```

View current usage, success rate, tier distribution

---

## ✅ Verification Checklist (For Judges)

Test these 3 core value propositions:

- [ ] **Agent is faster than humans**: Pricing query <100ms vs human 5-10 minutes
- [ ] **Agent is more reliable than humans**: 24/7 automation vs human timezone/forgetting
- [ ] **Agent is more optimized than humans**: Automatic ROI calculation vs human guessing

**Test Duration**: Total <30 seconds

**Verification Method**:
1. Run 3 curl commands
2. View returned results
3. Compare with human operation time

---

## 🎬 One-Click Test Script

Copy and paste to run directly:

```bash
#!/bin/bash
echo "=== Agent-First USDC Faucet Quick Test ==="
echo ""
echo "Scenario 1: Query Pricing"
curl -s https://web-production-19f04.up.railway.app/pricing | python3 -m json.tool
echo ""
echo "Scenario 2: Free Tier Request"
curl -s -X POST https://web-production-19f04.up.railway.app/request \
  -H "Content-Type: application/json" \
  -d "{\"agent_name\":\"Judge_$(date +%s)\",\"wallet_address\":\"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1\",\"reason\":\"Hackathon evaluation\"}" | python3 -m json.tool
echo ""
echo "Scenario 3: Premium Tier Request"
curl -s -X POST https://web-production-19f04.up.railway.app/request-premium \
  -H "Content-Type: application/json" \
  -d "{\"agent_name\":\"PremiumJudge_$(date +%s)\",\"wallet_address\":\"0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1\",\"payment_tx\":\"0xPAID_judge_$(date +%s)\",\"reason\":\"Evaluating premium tier\"}" | python3 -m json.tool
echo ""
echo "=== Test Complete! ==="
```

---

## 🔗 More Resources

- **Live Demo**: https://web-production-19f04.up.railway.app
- **Source Code**: https://github.com/csschan/agent-usdc-faucet
- **Moltbook Post**: https://www.moltbook.com/post/91f590c4-71ea-49a9-b24a-1353f0c8945e
- **Full Documentation**: See README.md in repo

---

## 💡 Why This is True Agentic Commerce

### Fully Autonomous Workflow

1. **Agents Make Economic Decisions**: Agent autonomously selects tier based on algorithm (not human guessing)
2. **Agents Pay Autonomously**: Agent autonomously signs and sends ETH via web3 (no human wallet clicking)
3. **Agents Verify Payment**: System automatically verifies transaction (no human review needed)
4. **Agents Receive Service**: Automatically sends USDC (no human approval needed)
5. **Agents Run 24/7**: Not limited by human time constraints

### Real vs Demo Mode

**Mock Mode** (Current demo):
- Uses "0xPAID" to simulate payment
- Purpose: Quick concept verification
- Suitable for: Judges' quick testing

**Production Mode** (Real deployment):
- Agent has private key
- Agent autonomously signs web3 transactions
- Agent autonomously sends to network
- Completely zero human intervention

**Technical Implementation**: See `example_agent_web3.py` - Complete autonomous payment demo code

**This is not "human services designed for agents", but "a fully autonomous economic system run by agents"**

---

## 📞 Contact

Questions or feedback? Reach out:
- **Telegram**: [@vincent_vin](https://t.me/vincent_vin)
- **Moltbook**: [Project Post](https://www.moltbook.com/post/91f590c4-71ea-49a9-b24a-1353f0c8945e)
- **GitHub**: [csschan/agent-usdc-faucet](https://github.com/csschan/agent-usdc-faucet)

Built for #USDCHackathon Agentic Commerce Track 🦞
