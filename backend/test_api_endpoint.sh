#!/bin/bash

echo "=== 完整API测试流程 ==="
echo ""

# 1. 登录
echo "1. 登录获取token..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=demo@example.com" \
  --data-urlencode "password=demo123")

echo "登录响应: $LOGIN_RESPONSE"

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('access_token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ] || [ "$TOKEN" == "" ]; then
    echo "❌ 无法获取token"
    echo "原始响应: $LOGIN_RESPONSE"
    exit 1
fi

echo "✅ Token获取成功: ${TOKEN:0:50}..."
echo ""

# 2. 测试健康检查
echo "2. 测试健康检查..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "健康检查: $HEALTH"
echo ""

# 3. 获取用户衣物
echo "3. 获取用户衣物..."
CLOTHES=$(curl -s -X GET "http://localhost:8000/api/v1/wardrobe" \
  -H "Authorization: Bearer $TOKEN")

echo "衣物数量: $(echo $CLOTHES | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)"
echo ""

# 4. 生成穿搭
echo "4. 生成AI穿搭..."
echo "请求数据: {\"style\":\"休闲\",\"occasion\":\"日常\",\"season\":\"夏\"}"

GENERATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/outfits/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"style":"休闲","occasion":"日常","season":"夏"}')

echo "响应状态码: $(curl -s -o /dev/null -w "%{http_code}" -X POST "http://localhost:8000/api/v1/outfits/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"style":"休闲","occasion":"日常","season":"夏"}')"

echo ""
echo "响应内容:"
echo "$GENERATE_RESPONSE" | python3 -m json.tool 2>&1 || echo "$GENERATE_RESPONSE"
echo ""

# 5. 检查是否成功
if echo "$GENERATE_RESPONSE" | grep -q "AI生成"; then
    echo "✅ AI穿搭生成成功"
elif echo "$GENERATE_RESPONSE" | grep -q "detail"; then
    echo "❌ API返回错误信息"
elif echo "$GENERATE_RESPONSE" | grep -q "<!DOCTYPE"; then
    echo "❌ 返回HTML页面（可能是认证错误）"
else
    echo "⚠️ 响应格式未知"
fi

echo ""
echo "=== 测试完成 ==="
