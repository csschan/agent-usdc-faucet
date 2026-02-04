"""
Database Module - SQLite for tracking faucet usage
Records all requests and enables analytics
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import json

logger = logging.getLogger(__name__)

DB_FILE = 'faucet.db'


class Database:
    """SQLite database for faucet requests and analytics"""

    def __init__(self, db_file: str = DB_FILE):
        """Initialize database connection"""
        self.db_file = db_file
        self.conn = None

    def init_db(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name

        cursor = self.conn.cursor()

        # Create requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                wallet_address TEXT NOT NULL,
                reason TEXT,
                amount REAL NOT NULL,
                tx_hash TEXT,
                moltbook_proof TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT TRUE
            )
        ''')

        # Create index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_name
            ON requests(agent_name)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON requests(timestamp)
        ''')

        self.conn.commit()
        logger.info(f"Database initialized: {self.db_file}")

    def record_request(
        self,
        agent_name: str,
        wallet_address: str,
        reason: str,
        amount: float,
        tx_hash: str,
        moltbook_proof: str = "",
        success: bool = True
    ):
        """Record a faucet request"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO requests
            (agent_name, wallet_address, reason, amount, tx_hash, moltbook_proof, success)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (agent_name, wallet_address, reason, amount, tx_hash, moltbook_proof, success))

        self.conn.commit()
        logger.info(f"Recorded request: {agent_name} -> {amount} USDC")

    def is_in_cooldown(self, agent_name: str, cooldown_hours: int) -> bool:
        """Check if agent is in cooldown period"""
        cursor = self.conn.cursor()

        # Calculate cooldown threshold
        threshold = datetime.now() - timedelta(hours=cooldown_hours)

        cursor.execute('''
            SELECT COUNT(*) as count
            FROM requests
            WHERE agent_name = ? AND timestamp > ? AND success = TRUE
        ''', (agent_name, threshold))

        result = cursor.fetchone()
        return result['count'] > 0

    def get_last_request_time(self, agent_name: str) -> str:
        """Get timestamp of last request from agent"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT timestamp
            FROM requests
            WHERE agent_name = ? AND success = TRUE
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (agent_name,))

        result = cursor.fetchone()
        return result['timestamp'] if result else "Never"

    def get_stats(self) -> Dict:
        """Get basic statistics"""
        cursor = self.conn.cursor()

        # Total requests
        cursor.execute('SELECT COUNT(*) as count FROM requests')
        total = cursor.fetchone()['count']

        # Total USDC sent
        cursor.execute('SELECT SUM(amount) as total FROM requests WHERE success = TRUE')
        result = cursor.fetchone()
        total_usdc = result['total'] if result['total'] else 0

        # Success rate
        cursor.execute('SELECT COUNT(*) as count FROM requests WHERE success = TRUE')
        successful = cursor.fetchone()['count']

        success_rate = (successful / total * 100) if total > 0 else 0

        return {
            'total_requests': total,
            'total_usdc': total_usdc,
            'success_rate': round(success_rate, 1)
        }

    def get_detailed_stats(self) -> Dict:
        """Get detailed statistics for dashboard"""
        cursor = self.conn.cursor()

        # Basic stats
        stats = self.get_stats()

        # Successful vs failed
        cursor.execute('SELECT COUNT(*) as count FROM requests WHERE success = TRUE')
        successful = cursor.fetchone()['count']

        cursor.execute('SELECT COUNT(*) as count FROM requests WHERE success = FALSE')
        failed = cursor.fetchone()['count']

        # Unique agents
        cursor.execute('SELECT COUNT(DISTINCT agent_name) as count FROM requests')
        unique_agents = cursor.fetchone()['count']

        # Use cases (categorize reasons)
        cursor.execute('SELECT reason FROM requests WHERE success = TRUE')
        reasons = cursor.fetchall()

        use_cases = self._categorize_use_cases([r['reason'] for r in reasons])

        return {
            **stats,
            'successful_requests': successful,
            'failed_requests': failed,
            'unique_agents': unique_agents,
            'use_cases': use_cases
        }

    def get_recent_requests(self, limit: int = 50) -> List[Dict]:
        """Get recent requests for display"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT agent_name, wallet_address, reason, amount, tx_hash, timestamp
            FROM requests
            WHERE success = TRUE
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        results = cursor.fetchall()

        return [dict(row) for row in results]

    def _categorize_use_cases(self, reasons: List[str]) -> List[Dict]:
        """
        Categorize request reasons into use cases

        Args:
            reasons: List of reason strings

        Returns:
            List of use case categories with counts
        """
        categories = {
            'Testing': 0,
            'Payment': 0,
            'Smart Contract': 0,
            'Agent-to-Agent': 0,
            'Hackathon': 0,
            'Other': 0
        }

        keywords = {
            'Testing': ['test', 'testing', 'try', 'experiment'],
            'Payment': ['payment', 'pay', 'transfer', 'send'],
            'Smart Contract': ['contract', 'deploy', 'smart contract'],
            'Agent-to-Agent': ['agent', 'a2a', 'agent-to-agent'],
            'Hackathon': ['hackathon', 'usdc', 'competition', 'project']
        }

        for reason in reasons:
            if not reason:
                categories['Other'] += 1
                continue

            reason_lower = reason.lower()
            categorized = False

            for category, kws in keywords.items():
                if any(kw in reason_lower for kw in kws):
                    categories[category] += 1
                    categorized = True
                    break

            if not categorized:
                categories['Other'] += 1

        # Convert to list with percentages
        total = len(reasons) if reasons else 1

        result = []
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                result.append({
                    'category': category,
                    'count': count,
                    'percentage': round(count / total * 100, 1)
                })

        return result
