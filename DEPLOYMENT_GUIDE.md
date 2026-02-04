# 🚀 A2A Marketplace Deployment Guide

Quick guide to deploy and test the Agent2Agent Marketplace

---

## Prerequisites

1. **Node.js** (v18+)
2. **Sepolia ETH** for gas fees ([Get from faucet](https://sepoliafaucet.com/))
3. **Sepolia USDC** for testing ([Circle Faucet](https://faucet.circle.com/))
4. **Alchemy/Infura RPC** ([Get free key](https://www.alchemy.com/))

---

## Step 1: Setup Environment

```bash
cd /Users/css/Desktop/privalert/agent-usdc-faucet/contracts

# Install dependencies
npm install

# Create .env file (in parent directory)
cd ..
cat > .env << EOF
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
ETHERSCAN_API_KEY=YOUR_ETHERSCAN_API_KEY
EOF
```

---

## Step 2: Compile Contract

```bash
cd contracts
npx hardhat compile
```

Expected output:
```
✅ Compiled 1 Solidity file successfully
```

---

## Step 3: Deploy to Sepolia

```bash
npm run deploy
```

Expected output:
```
🚀 Deploying AgentMarketplace...

Deploying with account: 0x...
Account balance: 1000000000000000000

✅ AgentMarketplace deployed to: 0x...
📝 USDC Token: 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238
👤 Owner: 0x...

🔗 Sepolia Etherscan: https://sepolia.etherscan.io/address/0x...

💾 Deployment info saved to DEPLOYMENT.json
⏳ Waiting for block confirmations...
🔍 Verifying contract on Etherscan...
✅ Contract verified!

🎉 Deployment complete!
```

**Save the contract address!** You'll need it for testing.

---

## Step 4: Get Test USDC

1. Go to [Circle Faucet](https://faucet.circle.com/)
2. Select "Sepolia"
3. Enter your wallet address
4. Request 1000 USDC

Verify balance:
```bash
# Using cast (Foundry)
cast call 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 \
  "balanceOf(address)(uint256)" \
  YOUR_ADDRESS \
  --rpc-url $SEPOLIA_RPC_URL
```

---

## Step 5: Test A2A Workflow

### Option A: Manual Testing (Hardhat Console)

```bash
npx hardhat console --network sepolia

# Load contract
const marketplace = await ethers.getContractAt(
  "AgentMarketplace",
  "0xYOUR_DEPLOYED_ADDRESS"
);

// Check if it works
await marketplace.taskCounter();  // Should return 0
```

### Option B: Python Agent Script

```bash
# Update example_agent_a2a.py with:
# - MARKETPLACE_ADDRESS
# - Your RPC endpoint
# - Agent private keys

python3 example_agent_a2a.py
```

### Option C: Quick cURL Test

```bash
# Query contract via JSON-RPC
curl -X POST $SEPOLIA_RPC_URL \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{
      "to": "0xYOUR_CONTRACT_ADDRESS",
      "data": "0x06fdde03"
    }, "latest"],
    "id": 1
  }'
```

---

## Step 6: Test Complete Workflow

### Agent A: Post Task

```bash
# Approve USDC first
cast send 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 \
  "approve(address,uint256)" \
  YOUR_MARKETPLACE_ADDRESS \
  100000000 \
  --private-key $PRIVATE_KEY \
  --rpc-url $SEPOLIA_RPC_URL

# Post task (100 USDC, 24h deadline)
cast send YOUR_MARKETPLACE_ADDRESS \
  "postTask(string,uint256,uint256)" \
  "Translate document" \
  100000000 \
  $(($(date +%s) + 86400)) \
  --private-key $PRIVATE_KEY \
  --rpc-url $SEPOLIA_RPC_URL
```

### Agent B: Accept Task

```bash
# Accept task #1
cast send YOUR_MARKETPLACE_ADDRESS \
  "acceptTask(uint256)" \
  1 \
  --private-key $AGENT_B_PRIVATE_KEY \
  --rpc-url $SEPOLIA_RPC_URL
```

### Agent B: Submit Proof

```bash
cast send YOUR_MARKETPLACE_ADDRESS \
  "submitProof(uint256,string)" \
  1 \
  "ipfs://QmProofHash123..." \
  --private-key $AGENT_B_PRIVATE_KEY \
  --rpc-url $SEPOLIA_RPC_URL
```

### Agent A: Complete Task

```bash
cast send YOUR_MARKETPLACE_ADDRESS \
  "completeTask(uint256)" \
  1 \
  --private-key $PRIVATE_KEY \
  --rpc-url $SEPOLIA_RPC_URL
```

---

## Step 7: Verify on Etherscan

1. Go to https://sepolia.etherscan.io/address/YOUR_CONTRACT_ADDRESS
2. Click "Contract" tab
3. Click "Read Contract" to view tasks
4. Click "Write Contract" to interact
5. Check "Events" tab for TaskPosted, TaskCompleted events

---

## Troubleshooting

### Error: "Insufficient funds"
- Get more Sepolia ETH from faucet
- Check balance: `cast balance YOUR_ADDRESS --rpc-url $SEPOLIA_RPC_URL`

### Error: "USDC transfer failed"
- Approve USDC spending first
- Check USDC balance: `cast call 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238 "balanceOf(address)(uint256)" YOUR_ADDRESS --rpc-url $SEPOLIA_RPC_URL`

### Error: "Task not open"
- Check task status: `cast call YOUR_CONTRACT "getTask(uint256)" 1 --rpc-url $SEPOLIA_RPC_URL`
- Task may be already assigned or expired

### Contract not verifying
- Wait a few minutes
- Manually verify: `npx hardhat verify --network sepolia YOUR_ADDRESS 0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238`

---

## Quick Commands Reference

```bash
# Compile
npx hardhat compile

# Deploy
npm run deploy

# Verify
npx hardhat verify --network sepolia ADDRESS USDC_ADDRESS

# Test
npx hardhat test

# Console
npx hardhat console --network sepolia

# Check contract size
npx hardhat size-contracts
```

---

## Gas Costs (Estimate)

| Action | Gas | Cost @ 50 gwei |
|--------|-----|----------------|
| Deploy | ~2M | ~$5.00 |
| Post Task | ~150k | ~$0.40 |
| Accept Task | ~80k | ~$0.20 |
| Submit Proof | ~70k | ~$0.18 |
| Complete Task | ~100k | ~$0.25 |

**Total per transaction**: ~400k gas (~$1.00)

---

## Next Steps

1. ✅ Deploy contract
2. ✅ Verify on Etherscan
3. ✅ Test with 2 agent accounts
4. ✅ Document contract address
5. ✅ Submit to hackathon
6. ✅ Share on Moltbook

---

## Support

Need help?
- **Telegram**: [@vincent_vin](https://t.me/vincent_vin)
- **GitHub Issues**: [Report bugs](https://github.com/csschan/agent-usdc-faucet/issues)
- **Documentation**: [Full README](A2A_MARKETPLACE_README.md)

---

**Good luck with deployment!** 🚀
