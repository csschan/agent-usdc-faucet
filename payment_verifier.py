"""
Payment Verification Module
Verifies ETH payments for premium tier access
"""

from web3 import Web3
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PaymentVerifier:
    """Verify ETH payments for premium faucet access"""

    def __init__(self, payment_address: str, rpc_url: str = None):
        """
        Initialize payment verifier

        Args:
            payment_address: Faucet payment receiving address
            rpc_url: Optional Sepolia RPC URL for real verification
        """
        self.payment_address = payment_address
        self.rpc_url = rpc_url

        if rpc_url:
            self.w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not self.w3.is_connected():
                logger.warning(f"Failed to connect to RPC: {rpc_url}")
                self.w3 = None
        else:
            self.w3 = None

        logger.info(f"Payment verifier initialized: {payment_address}")

    def verify_payment(self, tx_hash: str, expected_amount_eth: float = 0.001) -> dict:
        """
        Verify a payment transaction

        Args:
            tx_hash: Transaction hash to verify
            expected_amount_eth: Expected payment amount in ETH

        Returns:
            dict with verification result and details
        """
        if not self.w3:
            # No RPC - can't verify
            return {
                'verified': False,
                'error': 'No RPC configured - cannot verify payment'
            }

        try:
            # Get transaction details
            tx = self.w3.eth.get_transaction(tx_hash)

            if not tx:
                return {'verified': False, 'error': 'Transaction not found'}

            # Check recipient
            if tx['to'].lower() != self.payment_address.lower():
                return {
                    'verified': False,
                    'error': f'Payment sent to wrong address: {tx["to"]}'
                }

            # Check amount
            amount_eth = self.w3.from_wei(tx['value'], 'ether')
            if amount_eth < expected_amount_eth:
                return {
                    'verified': False,
                    'error': f'Insufficient payment: {amount_eth} ETH (need {expected_amount_eth} ETH)'
                }

            # Check confirmation
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            if receipt['status'] != 1:
                return {'verified': False, 'error': 'Transaction failed'}

            current_block = self.w3.eth.block_number
            confirmations = current_block - receipt['blockNumber']

            if confirmations < 1:
                return {
                    'verified': False,
                    'error': f'Need at least 1 confirmation (current: {confirmations})'
                }

            # All checks passed
            return {
                'verified': True,
                'amount_eth': float(amount_eth),
                'from_address': tx['from'],
                'confirmations': confirmations,
                'block_number': receipt['blockNumber']
            }

        except Exception as e:
            logger.error(f"Payment verification error: {e}")
            return {'verified': False, 'error': str(e)}

    def get_recent_payments(self, from_address: str = None, hours: int = 24) -> list:
        """
        Get recent payments to faucet

        Args:
            from_address: Optional filter by sender
            hours: Look back this many hours

        Returns:
            List of payment transactions
        """
        if not self.w3:
            return []

        try:
            current_block = self.w3.eth.block_number
            # Rough estimate: 12s per block on Sepolia
            blocks_per_hour = 300
            from_block = current_block - (blocks_per_hour * hours)

            # This is simplified - in production use event logs
            # For now just return empty list
            return []

        except Exception as e:
            logger.error(f"Error fetching recent payments: {e}")
            return []


class MockPaymentVerifier(PaymentVerifier):
    """Mock payment verifier for testing"""

    def __init__(self):
        """Initialize mock verifier"""
        self.payment_address = "0x0000000000000000000000000000000000000001"
        logger.info("Mock payment verifier initialized")

    def verify_payment(self, tx_hash: str, expected_amount_eth: float = 0.001) -> dict:
        """
        Mock payment verification

        Rules:
        - Any tx hash starting with "0xPAID" is considered valid payment
        - Otherwise returns verification failure
        """
        if not tx_hash.startswith('0x'):
            return {'verified': False, 'error': 'Invalid transaction hash format'}

        # Accept special mock payment hashes (case-insensitive after 0x)
        if tx_hash.startswith('0x') and tx_hash[2:].upper().startswith('PAID'):
            logger.info(f"[MOCK] Payment verified: {tx_hash}")
            return {
                'verified': True,
                'amount_eth': expected_amount_eth,
                'from_address': '0x' + '1' * 40,
                'confirmations': 3,
                'block_number': 123456
            }

        # Reject other hashes
        return {
            'verified': False,
            'error': 'Mock payment not recognized. Use tx hash starting with "0xPAID" for testing.'
        }

    def get_recent_payments(self, from_address: str = None, hours: int = 24) -> list:
        """Mock recent payments - return empty list"""
        return []
