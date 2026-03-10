#!/bin/bash

echo "=== 测试添加衣物功能 ==="
echo ""

# 1. 登录获取token
echo "1. 用户登录..."
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=demo@example.com" \
  --data-urlencode "password=demo123" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")

if [ -z "$TOKEN" ]; then
    echo "❌ 登录失败：无法获取token"
    exit 1
fi

echo "✅ 登录成功"
echo ""

# 2. 先上传图片（模拟）
echo "2. 模拟添加衣物（使用测试图片URL）..."
CLOTHING_DATA='{
  "name": "白色T恤",
  "category": "上衣",
  "color": "[\"白色\", \"黑色\"]",
  "style": "[\"休闲\"]",
  "season": "[\"夏\"]",
  "brand": "Uniqlo",
  "size": "M",
  "material": "棉",
  "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
}'

echo "衣物数据: $CLOTHING_DATA"
echo ""

# 3. 添加衣物
echo "3. 发送添加衣物请求..."
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/wardrobe" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "$CLOTHING_DATA")

echo "服务器响应: $RESPONSE"
echo ""

# 4. 检查是否成功
if echo "$RESPONSE" | grep -q "白色T恤"; then
    echo "✅ 添加衣物成功！"

    # 提取衣物ID
    CLOTHING_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
    echo "衣物ID: $CLOTHING_ID"
else
    echo "❌ 添加衣物失败"
fi

echo ""

# 5. 查看衣物列表
echo "4. 查看用户衣物列表..."
CLOTHES_LIST=$(curl -s -X GET "http://localhost:8000/api/v1/wardrobe" \
  -H "Authorization: Bearer $TOKEN")

echo "$CLOTHES_LIST" | python3 -m json.tool
echo ""

echo "=== 测试完成 ==="
