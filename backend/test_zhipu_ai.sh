#!/bin/bash

echo "=== 智谱AI GLM-4V 穿搭推荐测试 ==="
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

# 2. 添加一些测试衣物
echo "2. 添加测试衣物..."

# 添加上衣
curl -s -X POST "http://localhost:8000/api/v1/wardrobe" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "白色简约T恤",
    "category": "上衣",
    "color": "[\"白色\"]",
    "style": "[\"休闲\", \"简约\"]",
    "season": "[\"春\", \"夏\"]",
    "brand": "Uniqlo",
    "size": "M",
    "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
  }' > /dev/null

# 添加裤子
curl -s -X POST "http://localhost:8000/api/v1/wardrobe" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "黑色休闲裤",
    "category": "裤子",
    "color": "[\"黑色\"]",
    "style": "[\"休闲\"]",
    "season": "[\"春\", \"夏\", \"秋\"]",
    "brand": "Zara",
    "size": "M",
    "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400"
  }' > /dev/null

# 添加鞋子
curl -s -X POST "http://localhost:8000/api/v1/wardrobe" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "白色运动鞋",
    "category": "鞋子",
    "color": "[\"白色\"]",
    "style": "[\"运动\", \"休闲\"]",
    "season": "[\"春\", \"夏\", \"秋\"]",
    "brand": "Nike",
    "size": "42",
    "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
  }' > /dev/null

echo "✅ 测试衣物添加完成"
echo ""

# 3. 查看衣物列表
echo "3. 查看当前衣物列表："
CLOTHES=$(curl -s -X GET "http://localhost:8000/api/v1/wardrobe" \
  -H "Authorization: Bearer $TOKEN")

echo "$CLOTHES" | python3 -m json.tool
echo ""

# 4. 测试AI生成穿搭
echo "4. 测试智谱AI生成穿搭..."
echo "请求参数: 风格=休闲, 场合=日常, 季节=夏"
echo ""

GENERATE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/outfits/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "style": "休闲",
    "occasion": "日常",
    "season": "夏"
  }')

echo "AI生成响应:"
echo "$GENERATE_RESPONSE" | python3 -m json.tool
echo ""

# 5. 检查是否成功
if echo "$GENERATE_RESPONSE" | grep -q "AI生成"; then
    echo "✅ AI穿搭生成成功！"
    OUTFIT_ID=$(echo "$GENERATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
    echo "穿搭ID: $OUTFIT_ID"
else
    echo "❌ AI穿搭生成失败"
fi

echo ""
echo "=== 测试完成 ==="
echo ""
echo "📝 说明："
echo "- 如果未配置智谱AI API Key，系统将返回模拟响应"
echo "- 配置API Key后，将使用GLM-4V模型生成真实的穿搭建议"
echo "- 修改.env文件中的TONGYI_API_KEY配置项即可"
echo ""
echo "🔗 相关文档："
echo "- 配置说明: /var/www/ootd/backend/ZHIPU_AI_SETUP.md"
echo "- 智谱AI官网: https://open.bigmodel.cn/"
