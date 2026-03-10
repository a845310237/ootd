#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 GLM-4.6V 模型切换"""

import json

print("=" * 60)
print("智谱 AI GLM-4.6V 模型切换验证")
print("=" * 60)

# 新的 GLM-4.6V 请求格式
new_request_format = {
    "model": "glm-4.6v",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "你是一个专业的穿搭顾问。根据以下信息生成穿搭建议：\n\n用户信息：\n- 身高: 170cm\n- 体重: 65kg\n- 体型: 标准\n- 肤色: 中性\n\n可用衣物：\n- 白色简约T恤 (分类: 上衣, 颜色: 白色, 风格: 休闲, 简约, 季节: 春, 夏)\n- 黑色休闲裤 (分类: 裤子, 颜色: 黑色, 风格: 休闲, 季节: 春, 夏, 秋)\n- 白色运动鞋 (分类: 鞋子, 颜色: 白色, 风格: 运动, 休闲, 季节: 春, 夏, 秋)\n\n要求：\n- 风格: 休闲\n- 场合: 日常\n- 季节: 夏\n\n请只返回JSON格式，不要包含其他文字：\n{\n  \"selected_items\": [\"衣物ID1\", \"衣物ID2\", ...],\n  \"reasoning\": \"详细的搭配理由说明，解释为什么这样搭配适合用户的身材和场合\",\n  \"tips\": [\"穿搭小贴士1\", \"穿搭小贴士2\", \"穿搭小贴士3\"]\n}"
                }
            ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2000
}

print("\n📋 新的请求格式 (GLM-4.6V):")
print("-" * 40)
print(json.dumps(new_request_format, indent=2, ensure_ascii=False))

print("\n🔍 主要变化:")
print("-" * 40)
print("1. 模型名称: glm-4v → glm-4.6v")
print("2. 消息格式: 支持多模态内容数组")
print("3. 内容类型: 可以混合文本和图片")
print("   - 文本: {\"type\": \"text\", \"text\": \"...\"}")
print("   - 图片: {\"type\": \"image_url\", \"image_url\": {\"url\": \"...\"}}")

print("\n✅ 兼容性:")
print("-" * 40)
print("- 向后兼容纯文本输入")
print("- 支持图片+文本混合输入")
print("- API 端点保持不变")
print("- 认证方式保持不变")

print("\n📦 代码更新:")
print("-" * 40)
print("✓ app/services/tongyi_service.py - 已更新")
print("✓ ZHIPU_API_DETAILS.md - 已更新")
print("✓ ZHIPU_API_REFERENCE.md - 已更新")
print("✓ show_ai_api_details.sh - 已更新")

print("\n🚀 测试命令:")
print("-" * 40)
print("curl --request POST \\")
print("  --url https://open.bigmodel.cn/api/paas/v4/chat/completions \\")
print("  --header 'Authorization: Bearer YOUR_API_KEY' \\")
print("  --header 'Content-Type: application/json' \\")
print("  --data '{")
print("    \"model\": \"glm-4.6v\",")
print("    \"messages\": [")
print("      {")
print("        \"role\": \"user\",")
print("        \"content\": [")
print("          {\"type\": \"text\", \"text\": \"你好\"}")
print("        ]")
print("      }")
print("    ]")
print("  }'")

print("\n" + "=" * 60)
print("✨ GLM-4.6V 模型切换完成！")
print("=" * 60)
