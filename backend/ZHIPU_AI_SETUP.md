# 智谱AI GLM-4V 穿搭推荐集成说明

## 概述

已成功将AI穿搭推荐接口从通义万相替换为智谱AI的GLM-4V模型。

## 配置步骤

### 1. 获取智谱AI API Key

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录账号
3. 在控制台创建API Key
4. 复制API Key

### 2. 配置环境变量

编辑 `.env` 文件，更新API Key：

```env
# 智谱AI API配置
TONGYI_API_KEY=your-actual-zhipu-api-key-here
ZHIPU_API_KEY=your-actual-zhipu-api-key-here
```

**注意**: 复用原有的 `TONGYI_API_KEY` 配置项，填入智谱AI的API Key即可。

### 3. 重启应用

```bash
# 停止当前应用
pkill -f "uvicorn app.main:app"

# 启动应用
cd /var/www/ootd/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## GLM-4V 模型特性

### 视觉理解能力
- 支持图片上传和分析
- 理解衣物颜色、款式、材质
- 分析身材特征和穿搭风格

### 文本生成能力
- 专业的穿搭建议
- 详细的搭配理由
- 实用的穿搭小贴士

## API 调用示例

### 端点
```
POST /api/v1/outfits/generate
```

### 请求示例
```json
{
  "style": "休闲",
  "occasion": "日常",
  "season": "春"
}
```

### 响应示例
```json
{
  "id": "outfit-id",
  "name": "AI生成: 休闲穿搭",
  "style": "休闲",
  "occasion": "日常",
  "season": "春",
  "ai_generated": true,
  "reasoning": "根据您的身材特征和休闲风格...",
  "tips": ["建议搭配简约配饰", "注意层次感"],
  "items": [...]
}
```

## 提示词优化

当前提示词包含以下信息：
- 用户身材信息（身高、体重、体型、肤色）
- 可用衣物列表（分类、颜色、风格、季节）
- 穿搭要求（风格、场合、季节）

可以根据实际效果进一步优化提示词，提高推荐质量。

## 费用说明

GLM-4V 按使用量计费：
- 输入Token费用
- 输出Token费用
- 具体价格请参考智谱AI官网

建议：
- 设置合理的Token限制
- 监控API使用量
- 优化提示词长度

## 错误处理

### API Key 未配置
如果API Key未配置或错误，系统会返回模拟响应：
- 从不同分类选择衣物
- 生成通用的搭配建议
- 返回标准穿搭小贴士

### API 调用失败
如果API调用失败，会自动降级到模拟响应，确保功能可用。

## 测试

### 1. 添加测试衣物
```bash
curl -X POST "http://localhost:8000/api/v1/wardrobe" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "白色T恤",
    "category": "上衣",
    "color": "[\"白色\"]",
    "style": "[\"休闲\"]",
    "season": "[\"夏\"]",
    "image_url": "https://example.com/shirt.jpg"
  }'
```

### 2. 生成AI穿搭
```bash
curl -X POST "http://localhost:8000/api/v1/outfits/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "style": "休闲",
    "occasion": "日常",
    "season": "夏"
  }'
```

## 后续优化

1. **图片分析增强**: 利用GLM-4V的视觉能力，直接分析衣物图片
2. **多轮对话**: 支持用户与AI进行多轮对话优化推荐
3. **个性化学习**: 根据用户反馈优化推荐算法
4. **批量生成**: 支持一次性生成多个穿搭方案

## 技术支持

- 智谱AI文档: https://open.bigmodel.cn/dev/api
- GLM-4V模型文档: https://open.bigmodel.cn/dev/api#glm-4v
- 问题反馈: 查看服务器日志 `/var/www/ootd/backend/server.log`
