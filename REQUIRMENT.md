# 穿搭AI (OOTD)

智能穿搭助手，为你打造个性化穿搭方案。基于 Next.js 构建的现代化穿搭推荐应用。

## 项目简介

穿搭AI 是一个智能化的个人穿搭管理平台，帮助用户数字化管理衣橱，并通过 AI 技术生成个性化的穿搭建议。

### 核心功能

- **👔 衣物管理** - 数字化你的衣物，轻松管理每一件单品
- **🤖 AI 智能搭配** - 基于你的身材特征和场合需求，AI 生成专属穿搭建议
- **✨ DIY 穿搭** - 自由组合衣物，创建属于你的独特风格
- **📊 穿搭记录** - 保存和回顾你的所有穿搭方案

## 技术栈

### 前端框架
- elementui

### 后端框架
- python fastapi

### 数据库

- mysql

### AI 集成
- **minimax image-01 **

    curl --request POST \
      --url https://api.minimaxi.com/v1/image_generation \
      --header 'Authorization: Bearer <token>' \
      --header 'Content-Type: application/json' \
      --data '
    {
      "model": "image-01",
      "prompt": "A man in a white t-shirt, full-body, standing front view, outdoors, with the Venice Beach sign in the background, Los Angeles. Fashion photography in 90s documentary style, film grain, photorealistic.",
      "aspect_ratio": "16:9",
      "response_format": "url",
      "n": 3,
      "prompt_optimizer": true
    }
    '

