#!/bin/bash

echo "=========================================="
echo "🚀 启动Mock模式测试服务器"
echo "=========================================="

# 启动服务器（后台）
python3 -c "
from app_test import app, db
db.init_db()
print('✅ 数据库初始化完成')
print('🌐 服务器运行在: http://localhost:5000')
print('📝 访问 http://localhost:5000 查看主页')
print('')
app.run(host='0.0.0.0', port=5000, debug=False)
" &

SERVER_PID=$!
echo "服务器PID: $SERVER_PID"

# 等待服务器启动
sleep 3

echo ""
echo "=========================================="
echo "🧪 测试API端点"
echo "==========================================

"

# 1. 健康检查
echo "1️⃣ 健康检查:"
curl -s http://localhost:5000/health 2>/dev/null | python3 -m json.tool 2>/dev/null || echo "等待服务器启动..."
echo ""

sleep 2

# 2. 请求USDC
echo "2️⃣ 请求10 USDC:"
curl -s -X POST http://localhost:5000/request \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "Galeon", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Testing for USDC hackathon"}' \
  | python3 -m json.tool
echo ""

# 3. 查看统计
echo "3️⃣ 查看统计:"
curl -s http://localhost:5000/stats | python3 -m json.tool
echo ""

# 4. 测试冷却
echo "4️⃣ 测试冷却（应该被拒绝）:"
curl -s -X POST http://localhost:5000/request \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "Galeon", "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1", "reason": "Second request"}' \
  | python3 -m json.tool
echo ""

echo "=========================================="
echo "✅ 测试完成！"
echo "=========================================="
echo ""
echo "服务器仍在运行，访问: http://localhost:5000"
echo "按Ctrl+C停止服务器，或运行: kill $SERVER_PID"
echo ""

# 保持脚本运行，等待用户手动停止
wait $SERVER_PID
