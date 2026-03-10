#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '/var/www/ootd/backend')

print("=== 测试生成穿搭API ===")

try:
    from app.services.wardrobe_service import get_user_clothes
    from app.models.database import SessionLocal

    # 获取数据库会话
    db = SessionLocal()

    # 获取测试用户
    user = db.query(__import__('app.models.user', fromlist=['User']).User).filter(
        __import__('app.models.user', fromlist=['User']).User.email == "demo@example.com"
    ).first()

    if not user:
        print("❌ 测试用户不存在")
        sys.exit(1)

    print(f"✅ 用户ID: {user.id}")

    # 获取用户衣物
    clothes = get_user_clothes(db, user.id)
    print(f"✅ 用户衣物数量: {len(clothes)}")

    if len(clothes) == 0:
        print("❌ 没有衣物，无法测试")
        sys.exit(1)

    # 打印衣物信息
    for c in clothes[:3]:
        print(f"  - {c.name} ({c.category})")

    db.close()

    # 测试AI服务
    from app.services.tongyi_service import (
        ZhipuClothingItem,
        ZhipuUser,
        ZhipuRequirements,
        generate_outfit_recommendation
    )

    clothing_items = [
        ZhipuClothingItem(
            id=c.id,
            name=c.name,
            category=c.category,
            color=eval(c.color) if c.color else [],
            style=eval(c.style) if c.style else [],
            season=eval(c.season) if c.season else [],
            imageUrl=c.image_url
        ) for c in clothes[:3]
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

    print("\n调用AI服务...")
    result = generate_outfit_recommendation(
        user_info,
        clothing_items,
        requirements
    )

    print(f"✅ AI服务调用成功")
    print(f"选中衣物: {result.selected_items}")
    print(f"搭配理由: {result.reasoning[:100]}...")
    print(f"穿搭小贴士: {result.tips}")

except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
