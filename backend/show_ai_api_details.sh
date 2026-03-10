#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谱AI GLM-4V API调用详情展示
"""

print("=" * 60)
print("智谱AI GLM-4V 穿搭推荐API调用详情")
print("=" * 60)

print("\n📍 API端点信息:")
print("-" * 40)
print("URL: https://open.bigmodel.cn/api/paas/v4/chat/completions")
print("方法: POST")
print("模型: glm-4.6v (最新版本，支持多模态)")

print("\n🔑 认证方式:")
print("-" * 40)
print("Header: Authorization: Bearer YOUR_API_KEY")
print("获取方式: https://open.bigmodel.cn/")

print("\n📤 请求格式:")
print("-" * 40)
print(json.dumps({
    "model": "glm-4.6v",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "你是一个专业的穿搭顾问..."
                }
            ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2000
}, indent=2, ensure_ascii=False))

print("\n💡 提示词结构:")
print("-" * 40)
prompt_template = """你是一个专业的穿搭顾问。根据以下信息生成穿搭建议：

用户信息：
- 身高: 170cm
- 体重: 65kg
- 体型: 标准
- 肤色: 中性

可用衣物：
- 白色简约T恤 (分类: 上衣, 颜色: 白色, 风格: 休闲, 简约, 季节: 春, 夏)
- 黑色休闲裤 (分类: 裤子, 颜色: 黑色, 风格: 休闲, 季节: 春, 夏, 秋)
- 白色运动鞋 (分类: 鞋子, 颜色: 白色, 风格: 运动, 休闲, 季节: 春, 夏, 秋)

要求：
- 风格: 休闲
- 场合: 日常
- 季节: 夏

请只返回JSON格式，不要包含其他文字：
{
  "selected_items": ["衣物ID1", "衣物ID2", ...],
  "reasoning": "详细的搭配理由说明",
  "tips": ["穿搭小贴士1", "穿搭小贴士2"]
}"""

print(prompt_template)

print("\n📥 响应格式:")
print("-" * 40)
print(json.dumps({
    "choices": [
        {
            "message": {
                "content": "{\n  \"selected_items\": [\"id1\", \"id2\"],\n  \"reasoning\": \"搭配理由\",\n  \"tips\": [\"小贴士1\", \"小贴士2\"]\n}"
            }
        }
    ]
}, indent=2, ensure_ascii=False))

print("\n⚙️ 配置参数:")
print("-" * 40)
print("temperature: 0.7      # 控制随机性，0-1，越高越随机")
print("top_p: 0.9           # 核采样，0-1，控制多样性")
print("max_tokens: 2000     # 最大输出token数")

print("\n🔧 代码实现位置:")
print("-" * 40)
print("文件: app/services/tongyi_service.py")
print("函数: call_zhipu_api()")
print("入口: generate_outfit_recommendation()")

print("\n📋 调用流程:")
print("-" * 40)
print("1. 用户在前端选择穿搭要求（风格、场合、季节）")
print("2. 前端发送POST请求到 /api/v1/outfits/generate")
print("3. 后端获取用户的衣物列表")
print("4. 构建智谱AI请求（用户信息+衣物+需求）")
print("5. 调用智谱AI GLM-4V API")
print("6. 解析AI响应（JSON提取）")
print("7. 创建穿搭记录并保存到数据库")
print("8. 返回穿搭详情给前端")

print("\n💰 费用说明:")
print("-" * 40)
print("- GLM-4V按输入和输出token计费")
print("- 输入: 提示词token数")
print("- 输出: 生成内容的token数")
print("- 查询价格: https://open.bigmodel.cn/price")

print("\n🚀 使用示例:")
print("-" * 40)
print("1. 获取API Key: https://open.bigmodel.cn/")
print("2. 更新.env文件:")
print("   TONGYI_API_KEY=your-actual-zhipu-api-key")
print("3. 重启应用即可启用真实AI推荐")

print("\n📞 当前状态:")
print("-" * 40)
print("模拟模式: 使用智能算法选择衣物")
print("真实模式: 配置API Key后使用GLM-4V模型")

print("\n" + "=" * 60)
print("详细配置请查看: /var/www/ootd/backend/ZHIPU_AI_SETUP.md")
print("=" * 60)
