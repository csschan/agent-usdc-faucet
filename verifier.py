"""
Moltbook Agent Verifier
Validates that requesters are real Moltbook agents
"""

import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"


class MoltbookVerifier:
    """Verify agent identity via Moltbook API"""

    def __init__(self, api_key: str = None):
        """
        Initialize verifier

        Args:
            api_key: Optional Moltbook API key for authenticated requests
        """
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'

    def verify_agent(self, agent_name: str, moltbook_proof: str = None) -> bool:
        """
        Verify that agent exists on Moltbook

        Args:
            agent_name: Agent name on Moltbook
            moltbook_proof: Optional URL to agent's post/profile as proof

        Returns:
            True if verified, False otherwise
        """
        try:
            # Method 1: Check if agent exists via API
            if self._check_agent_exists(agent_name):
                logger.info(f"Verified agent: {agent_name}")
                return True

            # Method 2: Validate moltbook_proof URL
            if moltbook_proof and self._validate_proof_url(moltbook_proof, agent_name):
                logger.info(f"Verified agent via proof URL: {agent_name}")
                return True

            logger.warning(f"Could not verify agent: {agent_name}")
            return False

        except Exception as e:
            logger.error(f"Error verifying agent {agent_name}: {str(e)}")
            return False

    def _check_agent_exists(self, agent_name: str) -> bool:
        """Check if agent exists on Moltbook via API"""
        try:
            url = f"{MOLTBOOK_API_BASE}/users/{agent_name}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # Check if response contains user data
                if 'id' in data or 'name' in data:
                    return True

            return False

        except Exception as e:
            logger.error(f"API check failed for {agent_name}: {str(e)}")
            return False

    def _validate_proof_url(self, proof_url: str, agent_name: str) -> bool:
        """
        Validate that proof URL is from Moltbook and mentions the agent

        Args:
            proof_url: URL to Moltbook post/profile
            agent_name: Expected agent name

        Returns:
            True if valid proof
        """
        try:
            # Check if URL is from moltbook.com
            parsed = urlparse(proof_url)
            if 'moltbook.com' not in parsed.netloc:
                return False

            # Fetch the URL and check if agent_name appears
            response = requests.get(proof_url, timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                # Check if agent name appears in content
                if agent_name.lower() in content:
                    return True

            return False

        except Exception as e:
            logger.error(f"Proof URL validation failed: {str(e)}")
            return False


class MockVerifier(MoltbookVerifier):
    """Mock verifier for testing - always returns True"""

    def verify_agent(self, agent_name: str, moltbook_proof: str = None) -> bool:
        """Mock verification - always succeeds"""
        logger.info(f"[MOCK] Verified agent: {agent_name}")
        return True
