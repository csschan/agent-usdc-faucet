"""
测试混合定价模型
"""
from app_test import app
import json
import time
from threading import Thread
import urllib.request
import urllib.error


def test_api():
    """测试所有新的API端点"""
    time.sleep(2)  # Wait for server to start

    base_url = 'http://localhost:5001'

    # Test health endpoint
    print('=== Testing /health endpoint ===')
    try:
        req = urllib.request.Request(f'{base_url}/health')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f'Error: {e}')

    # Test pricing endpoint
    print('\n=== Testing /pricing endpoint ===')
    try:
        req = urllib.request.Request(f'{base_url}/pricing')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f'Error: {e}')

    # Test free tier
    print('\n=== Testing /request (Free tier) ===')
    try:
        req_data = {
            'agent_name': 'TestAgent',
            'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1',
            'reason': 'Testing free tier'
        }
        req = urllib.request.Request(
            f'{base_url}/request',
            data=json.dumps(req_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f'Error: {e}')

    # Test premium tier with valid payment
    print('\n=== Testing /request-premium (Premium tier - Valid payment) ===')
    try:
        req_data = {
            'agent_name': 'PremiumAgent',
            'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1',
            'payment_tx': '0xPAID1234567890abcdef',
            'reason': 'Testing premium tier'
        }
        req = urllib.request.Request(
            f'{base_url}/request-premium',
            data=json.dumps(req_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f'Error: {e}')

    # Test premium tier with invalid payment
    print('\n=== Testing /request-premium (Premium tier - Invalid payment) ===')
    try:
        req_data = {
            'agent_name': 'InvalidAgent',
            'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1',
            'payment_tx': '0x1234567890abcdef',  # Not starting with 0xPAID
            'reason': 'Testing invalid payment'
        }
        req = urllib.request.Request(
            f'{base_url}/request-premium',
            data=json.dumps(req_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        print(f'HTTP Error {e.code}:')
        print(json.dumps(json.loads(e.read()), indent=2))
    except Exception as e:
        print(f'Error: {e}')

    print('\n=== 测试完成 ===')


if __name__ == '__main__':
    # Start server in background thread
    def run_server():
        app.run(host='localhost', port=5001, debug=False, use_reloader=False)

    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()

    # Run tests
    test_api()
