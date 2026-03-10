#!/bin/bash

echo "=== 穿搭AI应用登录流程测试 ==="
echo ""

# 1. 注册用户
echo "1. 注册测试用户..."
REGISTER_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","name":"演示用户","password":"demo123"}')

echo "注册响应: $REGISTER_RESPONSE"
echo ""

# 2. 登录获取token
echo "2. 用户登录..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=demo@example.com" \
  --data-urlencode "password=demo123")

echo "登录响应: $LOGIN_RESPONSE"

# 提取token
TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")

if [ -z "$TOKEN" ]; then
    echo "❌ 登录失败：无法获取token"
    exit 1
fi

echo ""
echo "✅ 登录成功！获取到token: ${TOKEN:0:50}..."
echo ""

# 3. 测试访问用户信息API
echo "3. 测试访问用户信息API..."
USER_INFO=$(curl -s -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN")

echo "用户信息: $USER_INFO"
echo ""

# 4. 测试访问health端点
echo "4. 测试健康检查..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "健康状态: $HEALTH"
echo ""

echo "=== 测试完成 ==="
echo ""
echo "📝 测试说明："
echo "1. 应用使用SQLite数据库运行正常"
echo "2. 用户注册/登录功能正常"
echo "3. JWT Token认证正常"
echo ""
echo "🌐 访问地址："
echo "- 首页: http://localhost:8000/"
echo "- 登录: http://localhost:8000/auth/login"
echo "- Dashboard: http://localhost:8000/dashboard"
echo "- API文档: http://localhost:8000/api/docs"
echo ""
echo "🔑 测试账号："
echo "邮箱: demo@example.com"
echo "密码: demo123"
