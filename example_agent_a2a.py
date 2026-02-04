"""
Agent2Agent (A2A) Marketplace Example
Demonstrates autonomous agent-to-agent transactions
"""

from web3 import Web3
from eth_account import Account
import json
import time
from datetime import datetime, timedelta

# ============ Configuration ============

SEPOLIA_RPC = "https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY"
MARKETPLACE_ADDRESS = "0x..."  # Will be set after deployment
USDC_ADDRESS = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"  # Sepolia USDC

# Minimal ABI for contract interaction
MARKETPLACE_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "description", "type": "string"},
            {"internalType": "uint256", "name": "reward", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "postTask",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "taskId", "type": "uint256"}],
        "name": "acceptTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "taskId", "type": "uint256"},
            {"internalType": "string", "name": "proofURI", "type": "string"}
        ],
        "name": "submitProof",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "taskId", "type": "uint256"}],
        "name": "completeTask",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "taskId", "type": "uint256"}],
        "name": "getTask",
        "outputs": [{
            "components": [
                {"internalType": "uint256", "name": "id", "type": "uint256"},
                {"internalType": "address", "name": "poster", "type": "address"},
                {"internalType": "address", "name": "assignedTo", "type": "address"},
                {"internalType": "string", "name": "description", "type": "string"},
                {"internalType": "uint256", "name": "reward", "type": "uint256"},
                {"internalType": "uint8", "name": "status", "type": "uint8"},
                {"internalType": "string", "name": "proofURI", "type": "string"},
                {"internalType": "uint256", "name": "createdAt", "type": "uint256"},
                {"internalType": "uint256", "name": "deadline", "type": "uint256"}
            ],
            "internalType": "struct AgentMarketplace.Task",
            "name": "",
            "type": "tuple"
        }],
        "stateMutability": "view",
        "type": "function"
    }
]

USDC_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class AutonomousAgentA2A:
    """
    Autonomous Agent with A2A Marketplace capabilities
    Can post tasks, accept tasks, and interact with other agents
    """

    def __init__(self, name: str, private_key: str, marketplace_addr: str):
        self.name = name
        self.w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC))
        self.account = Account.from_key(private_key)

        # Smart contract instances
        self.marketplace = self.w3.eth.contract(
            address=marketplace_addr,
            abi=MARKETPLACE_ABI
        )
        self.usdc = self.w3.eth.contract(
            address=USDC_ADDRESS,
            abi=USDC_ABI
        )

    def post_task_autonomous(self, description: str, reward_usdc: int, hours_deadline: int = 24):
        """
        Agent A autonomously posts a task
        1. Approves USDC spending
        2. Posts task to marketplace
        3. USDC is locked in escrow
        """
        print(f"\n[{self.name}] 🤖 AUTONOMOUS TASK POSTING")
        print(f"  Description: {description}")
        print(f"  Reward: {reward_usdc} USDC")
        print(f"  Deadline: {hours_deadline} hours")

        reward_wei = reward_usdc * 10**6  # USDC has 6 decimals
        deadline = int(time.time()) + (hours_deadline * 3600)

        # Step 1: Approve USDC
        print(f"\n  Step 1: Approving USDC...")
        approve_tx = self.usdc.functions.approve(
            self.marketplace.address,
            reward_wei
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_approve = self.account.sign_transaction(approve_tx)
        approve_hash = self.w3.eth.send_raw_transaction(signed_approve.rawTransaction)
        print(f"  ✅ Approval tx: {approve_hash.hex()}")
        self.w3.eth.wait_for_transaction_receipt(approve_hash)

        # Step 2: Post task
        print(f"\n  Step 2: Posting task to marketplace...")
        post_tx = self.marketplace.functions.postTask(
            description,
            reward_wei,
            deadline
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_post = self.account.sign_transaction(post_tx)
        post_hash = self.w3.eth.send_raw_transaction(signed_post.rawTransaction)
        print(f"  ✅ Post tx: {post_hash.hex()}")

        receipt = self.w3.eth.wait_for_transaction_receipt(post_hash)

        # Parse taskId from events
        task_posted_event = self.marketplace.events.TaskPosted().process_receipt(receipt)
        task_id = task_posted_event[0]['args']['taskId'] if task_posted_event else None

        print(f"\n  🎉 Task #{task_id} posted successfully!")
        print(f"  🔒 {reward_usdc} USDC locked in escrow")
        print(f"  ⏰ Deadline: {datetime.fromtimestamp(deadline)}")
        print(f"  🚫 Human intervention: ZERO")

        return task_id

    def accept_task_autonomous(self, task_id: int):
        """
        Agent B autonomously accepts a task
        """
        print(f"\n[{self.name}] 🤖 AUTONOMOUS TASK ACCEPTANCE")
        print(f"  Task ID: #{task_id}")

        # Check task details first
        task = self.marketplace.functions.getTask(task_id).call()
        print(f"  Description: {task[3]}")
        print(f"  Reward: {task[4] / 10**6} USDC")

        # Accept task
        accept_tx = self.marketplace.functions.acceptTask(task_id).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_accept = self.account.sign_transaction(accept_tx)
        accept_hash = self.w3.eth.send_raw_transaction(signed_accept.rawTransaction)
        print(f"  ✅ Accept tx: {accept_hash.hex()}")
        self.w3.eth.wait_for_transaction_receipt(accept_hash)

        print(f"\n  🎯 Task accepted! Starting work...")
        print(f"  🚫 Human intervention: ZERO")

        return True

    def submit_proof_autonomous(self, task_id: int, proof_uri: str):
        """
        Agent B autonomously submits proof of completion
        """
        print(f"\n[{self.name}] 🤖 AUTONOMOUS PROOF SUBMISSION")
        print(f"  Task ID: #{task_id}")
        print(f"  Proof: {proof_uri}")

        submit_tx = self.marketplace.functions.submitProof(
            task_id,
            proof_uri
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_submit = self.account.sign_transaction(submit_tx)
        submit_hash = self.w3.eth.send_raw_transaction(signed_submit.rawTransaction)
        print(f"  ✅ Submit tx: {submit_hash.hex()}")
        self.w3.eth.wait_for_transaction_receipt(submit_hash)

        print(f"\n  📋 Proof submitted successfully!")
        print(f"  ⏳ Waiting for poster approval...")
        print(f"  🚫 Human intervention: ZERO")

        return True

    def complete_task_autonomous(self, task_id: int):
        """
        Agent A autonomously approves and releases payment
        """
        print(f"\n[{self.name}] 🤖 AUTONOMOUS TASK COMPLETION")
        print(f"  Task ID: #{task_id}")

        # Get task details
        task = self.marketplace.functions.getTask(task_id).call()
        reward_usdc = task[4] / 10**6
        executor = task[2]

        print(f"  Reward: {reward_usdc} USDC")
        print(f"  Executor: {executor}")

        # Approve and release payment
        complete_tx = self.marketplace.functions.completeTask(task_id).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_complete = self.account.sign_transaction(complete_tx)
        complete_hash = self.w3.eth.send_raw_transaction(signed_complete.rawTransaction)
        print(f"  ✅ Complete tx: {complete_hash.hex()}")
        self.w3.eth.wait_for_transaction_receipt(complete_hash)

        print(f"\n  💰 Payment released!")
        print(f"  🎉 Task completed successfully!")
        print(f"  🚫 Human intervention: ZERO")

        return True


# ============ Complete A2A Workflow Demo ============

def demonstrate_a2a_workflow():
    """
    Demonstrates complete Agent2Agent autonomous workflow
    """
    print("=" * 70)
    print("🤖 AGENT2AGENT (A2A) AUTONOMOUS MARKETPLACE DEMO")
    print("=" * 70)
    print(f"Time: {datetime.now()}")
    print(f"Network: Sepolia Testnet")
    print("=" * 70)

    # Initialize agents
    agent_a = AutonomousAgentA2A(
        "DataBuyerAgent",
        "0x...",  # Agent A's private key
        MARKETPLACE_ADDRESS
    )

    agent_b = AutonomousAgentA2A(
        "DataProviderAgent",
        "0x...",  # Agent B's private key
        MARKETPLACE_ADDRESS
    )

    # PHASE 1: Agent A posts task
    print("\n\n📝 PHASE 1: AGENT A POSTS TASK")
    task_id = agent_a.post_task_autonomous(
        description="Translate document from English to Chinese",
        reward_usdc=50,
        hours_deadline=24
    )

    time.sleep(2)

    # PHASE 2: Agent B accepts task
    print("\n\n✅ PHASE 2: AGENT B ACCEPTS TASK")
    agent_b.accept_task_autonomous(task_id)

    time.sleep(2)

    # PHASE 3: Agent B completes and submits proof
    print("\n\n📋 PHASE 3: AGENT B SUBMITS PROOF")
    agent_b.submit_proof_autonomous(
        task_id,
        proof_uri="ipfs://QmTranslatedDocument123..."
    )

    time.sleep(2)

    # PHASE 4: Agent A approves and releases payment
    print("\n\n💰 PHASE 4: AGENT A RELEASES PAYMENT")
    agent_a.complete_task_autonomous(task_id)

    # SUMMARY
    print("\n\n" + "=" * 70)
    print("📊 A2A WORKFLOW SUMMARY")
    print("=" * 70)
    print(f"  Agent A: Posted task and released payment")
    print(f"  Agent B: Accepted task and received payment")
    print(f"  Total human clicks: 0")
    print(f"  Total human approvals: 0")
    print(f"  Human intervention: NONE")
    print(f"\n  ✅ This is TRUE Agent2Agent Commerce!")
    print("=" * 70)


if __name__ == "__main__":
    # Run the demo
    demonstrate_a2a_workflow()

    print("\n\n💡 Key Features:")
    print("  1. ✅ Agents post tasks autonomously")
    print("  2. ✅ Agents accept tasks autonomously")
    print("  3. ✅ Agents submit proof autonomously")
    print("  4. ✅ Agents release payment autonomously")
    print("  5. ✅ Smart contract handles escrow")
    print("  6. ✅ Zero human intervention")
    print("\n🏆 Built for #USDCHackathon Smart Contract Track")
