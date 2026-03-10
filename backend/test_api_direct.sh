#!/bin/bash

echo "=== 直接测试智谱AI API ==="
echo ""

# 测试API调用
echo "测试模拟响应（未配置API Key）..."
python3 << 'EOF'
import sys
sys.path.insert(0, '/var/www/ootd/backend')

from app.services.tongyi_service import (
    ZhipuClothingItem,
    ZhipuUser,
    ZhipuRequirements,
    generate_outfit_recommendation
)

# 创建测试数据
clothing_items = [
    ZhipuClothingItem(
        id="1",
        name="白色T恤",
        category="上衣",
        color=["白色"],
        style=["休闲"],
        season=["夏"],
        imageUrl="https://example.com/shirt.jpg"
    ),
    ZhipuClothingItem(
        id="2",
        name="黑色裤子",
        category="裤子",
        color=["黑色"],
        style=["休闲"],
        season=["夏"],
        imageUrl="https://example.com/pants.jpg"
    )
]

user_info = ZhipuUser(
    height=170,
    weight=65,
    body_type="标准",
    skin_tone="中性"
)

requirements = ZhipuRequirements(
    style="休闲",
    occasion="日常",
    season="夏"
)

# 调用AI服务
try:
    result = generate_outfit_recommendation(
        user_info,
        clothing_items,
        requirements
    )

    print("✅ AI服务调用成功！")
    print(f"选择的衣物: {result.selected_items}")
    print(f"搭配理由: {result.reasoning[:100]}...")
    print(f"穿搭小贴士: {result.tips}")

except Exception as e:
    print(f"❌ AI服务调用失败: {e}")
    import traceback
    traceback.print_exc()
EOF

echo ""
echo "=== 测试完成 ==="
