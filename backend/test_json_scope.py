#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试问题代码段"""

import json

# 模拟数据
class MockClothing:
    def __init__(self):
        self.id = "123"
        self.name = "Test"
        self.category = "上衣"
        self.color = '["白色"]'
        self.style = '["休闲"]'
        self.season = '["夏"]'
        self.image_url = "http://example.com"

clothes = [MockClothing()]

try:
    # 这是有问题的代码段
    clothing_items = [
        {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "color": json.loads(c.color) if c.color else [],
            "style": json.loads(c.style) if c.style else [],
            "season": json.loads(c.season) if c.season else [],
            "imageUrl": c.image_url
        } for c in clothes
    ]

    print("✅ 代码执行成功")
    print(f"结果: {clothing_items}")

except NameError as e:
    print(f"❌ NameError: {e}")
except Exception as e:
    print(f"❌ Exception: {e}")
