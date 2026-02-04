"""
Blockchain Module - Sepolia USDC Faucet
Handles sending testnet USDC via web3.py
"""

from web3 import Web3
from eth_account import Account
import logging

logger = logging.getLogger(__name__)

# Sepolia Testnet USDC Contract Address
# This is a mock address - replace with actual Sepolia USDC address
USDC_CONTRACT_ADDRESS = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"  # Sepolia USDC

# Minimal ERC20 ABI for transfer function
ERC20_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]


class USDCFaucet:
    """USDC Testnet Faucet for sending to agents"""

    def __init__(self, private_key: str, rpc_url: str):
        """
        Initialize faucet with wallet private key and RPC URL

        Args:
            private_key: Faucet wallet private key (with testnet USDC)
            rpc_url: Sepolia RPC endpoint
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self.w3.is_connected():
            raise Exception(f"Failed to connect to RPC: {rpc_url}")

        # Load faucet account
        self.account = Account.from_key(private_key) if private_key else None
        self.address = self.account.address if self.account else None

        # Load USDC contract
        self.usdc_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(USDC_CONTRACT_ADDRESS),
            abi=ERC20_ABI
        )

        logger.info(f"Faucet initialized: {self.address}")
        logger.info(f"Connected to: {rpc_url}")

    def send_usdc(self, to_address: str, amount: float) -> str:
        """
        Send USDC to specified address

        Args:
            to_address: Recipient Ethereum address
            amount: Amount in USDC (e.g., 10 for 10 USDC)

        Returns:
            Transaction hash
        """
        if not self.account:
            raise Exception("Faucet account not configured")

        # Convert amount to wei (USDC has 6 decimals)
        decimals = self.usdc_contract.functions.decimals().call()
        amount_wei = int(amount * (10 ** decimals))

        # Prepare transaction
        to_checksum = Web3.to_checksum_address(to_address)

        # Build transaction
        tx = self.usdc_contract.functions.transfer(
            to_checksum,
            amount_wei
        ).build_transaction({
            'from': self.address,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'gas': 100000,  # Sufficient for ERC20 transfer
            'gasPrice': self.w3.eth.gas_price,
        })

        # Sign transaction
        signed_tx = self.account.sign_transaction(tx)

        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Wait for receipt (with timeout)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if receipt['status'] != 1:
            raise Exception(f"Transaction failed: {tx_hash.hex()}")

        logger.info(f"Sent {amount} USDC to {to_address}: {tx_hash.hex()}")

        return tx_hash.hex()

    def get_balance(self) -> float:
        """Get faucet USDC balance"""
        if not self.address:
            return 0.0

        decimals = self.usdc_contract.functions.decimals().call()
        balance_wei = self.usdc_contract.functions.balanceOf(self.address).call()
        balance = balance_wei / (10 ** decimals)

        return balance

    def is_valid_address(self, address: str) -> bool:
        """Check if address is valid Ethereum address"""
        try:
            Web3.to_checksum_address(address)
            return True
        except:
            return False


class MockUSDCFaucet(USDCFaucet):
    """
    Mock faucet for testing without real blockchain
    Returns fake transaction hashes
    """

    def __init__(self):
        """Initialize mock faucet"""
        self.address = "0x0000000000000000000000000000000000000000"
        logger.info("Mock faucet initialized (for testing)")

    def send_usdc(self, to_address: str, amount: float) -> str:
        """Mock USDC send - returns fake tx hash"""
        import hashlib
        import time

        # Generate fake but unique tx hash
        data = f"{to_address}{amount}{time.time()}"
        tx_hash = "0x" + hashlib.sha256(data.encode()).hexdigest()

        logger.info(f"[MOCK] Sent {amount} USDC to {to_address}: {tx_hash}")

        return tx_hash

    def get_balance(self) -> float:
        """Mock balance - always return 10000"""
        return 10000.0

    def is_valid_address(self, address: str) -> bool:
        """Mock validation - check basic format"""
        return address.startswith('0x') and len(address) == 42
