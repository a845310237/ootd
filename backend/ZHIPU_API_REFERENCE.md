# 智谱AI GLM-4V API调用测试

## 测试API连接

```bash
# 测试API Key是否有效 (GLM-4.6V)
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "glm-4.6v",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "你好"
          }
        ]
      }
    ],
    "max_tokens": 100
  }'
```

## 完整请求示例

### 穿搭推荐请求 (GLM-4.6V)
```bash
curl --request POST \
  --url https://open.bigmodel.cn/api/paas/v4/chat/completions \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "glm-4.6v",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "你是一个专业的穿搭顾问。根据以下信息生成穿搭建议：

用户信息：
- 身高: 170cm
- 体重: 65kg
- 体型: 标准
- 肤色: 中性

可用衣物：
- 白色T恤 (分类: 上衣, 颜色: 白色, 风格: 休闲, 季节: 夏)
- 黑色裤子 (分类: 裤子, 颜色: 黑色, 风格: 休闲, 季节: 夏)
- 白色运动鞋 (分类: 鞋子, 颜色: 白色, 风格: 运动, 季节: 夏)

要求：
- 风格: 休闲
- 场合: 日常
- 季节: 夏

请只返回JSON格式，不要包含其他文字：
{
  \"selected_items\": [\"id1\", \"id2\"],
  \"reasoning\": \"搭配理由\",
  \"tips\": [\"小贴士1\", \"小贴士2\"]
}"
          }
        ]
      }
    ]
  }'
```

### 使用Python SDK (GLM-4.6V)
```python
import zhipuai
from zhipuai import ZhipuAI

# 初始化客户端
client = ZhipuAI(api_key="YOUR_API_KEY")

# 调用GLM-4.6V (支持多模态)
response = client.chat.completions.create(
    model="glm-4.6v",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "你好"
                }
            ]
        }
    ],
    temperature=0.7,
    max_tokens=2000
)

print(response.choices[0].message.content)
```

## 错误处理

### 常见错误代码
- 401: API Key无效或过期
- 400: 请求参数错误
- 429: 请求频率超限
- 500: 服务器内部错误

### 配额限制
- 免费额度: 每天一定的免费tokens
- 付费: 根据使用量计费
- 限流: 根据等级设置RPM限制
