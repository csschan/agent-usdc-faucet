"""
Mock模式Flask服务器 - 用于测试，不需要真实RPC
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from blockchain import MockUSDCFaucet
from verifier import MockVerifier
from database import Database

app = Flask(__name__)
CORS(app)

# 使用Mock组件
db = Database("test_faucet.db")
verifier = MockVerifier()
faucet = MockUSDCFaucet()

FAUCET_AMOUNT = 10
COOLDOWN_HOURS = 24

@app.route('/')
def index():
    stats = db.get_stats()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent USDC Faucet - Mock Mode</title>
        <style>
            body {{
                font-family: monospace;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #0a0a0a;
                color: #00ff00;
            }}
            h1 {{ color: #ffff00; }}
            .stat {{ margin: 10px 0; }}
            .code {{
                background: #1a1a1a;
                padding: 15px;
                border-left: 3px solid #00ff00;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>🚰 Agent USDC Faucet (Mock Mode)</h1>
        <p style="color: #ff9900;">⚠️ 测试模式 - 不会发送真实USDC</p>

        <h2>📊 Stats</h2>
        <div class="stat">Total Requests: {stats['total_requests']}</div>
        <div class="stat">Total USDC: {stats['total_usdc']}</div>
        <div class="stat">Success Rate: {stats['success_rate']}%</div>

        <h2>🧪 Test API</h2>
        <div class="code">
curl -X POST http://localhost:5000/request \\
  -H "Content-Type: application/json" \\
  -d '{{
    "agent_name": "TestAgent",
    "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
    "reason": "Testing faucet"
  }}'
        </div>

        <h2>🔗 Endpoints</h2>
        <ul>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/stats">/stats</a> - Detailed stats (JSON)</li>
        </ul>
    </body>
    </html>
    """

@app.route('/request', methods=['POST'])
def request_usdc():
    try:
        data = request.get_json()

        agent_name = data.get('agent_name')
        wallet_address = data.get('wallet_address')
        reason = data.get('reason', 'No reason provided')

        if not agent_name or not wallet_address:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: agent_name, wallet_address'
            }), 400

        # 检查冷却
        if db.is_in_cooldown(agent_name, COOLDOWN_HOURS):
            last_time = db.get_last_request_time(agent_name)
            return jsonify({
                'success': False,
                'error': f'Cooldown active. Last request: {last_time}'
            }), 429

        # 验证（Mock总是通过）
        if not verifier.verify_agent(agent_name):
            return jsonify({
                'success': False,
                'error': 'Agent verification failed'
            }), 403

        # 发送USDC（Mock）
        tx_hash = faucet.send_usdc(wallet_address, FAUCET_AMOUNT)

        # 记录到数据库
        db.record_request(
            agent_name=agent_name,
            wallet_address=wallet_address,
            reason=reason,
            amount=FAUCET_AMOUNT,
            tx_hash=tx_hash,
            moltbook_proof="",
            success=True
        )

        return jsonify({
            'success': True,
            'amount': f'{FAUCET_AMOUNT} USDC',
            'tx_hash': tx_hash,
            'explorer': f'https://sepolia.etherscan.io/tx/{tx_hash}',
            'message': f'✅ Sent {FAUCET_AMOUNT} testnet USDC (Mock mode) 🦞',
            'note': 'This is mock mode - no real transactions sent'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats')
def stats():
    stats = db.get_detailed_stats()
    return jsonify(stats)

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'mode': 'mock',
        'faucet_balance': faucet.get_balance()
    })

if __name__ == '__main__':
    db.init_db()
    print("=" * 60)
    print("🚀 Mock模式服务器启动")
    print("=" * 60)
    print("访问: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
