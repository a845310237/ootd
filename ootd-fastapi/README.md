# 穿搭AI (OOTD) - FastAPI + Vue 3

智能穿搭助手，为你打造个性化穿搭方案。基于 FastAPI 和 Vue 3 构建的现代化穿搭推荐应用。

## 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **SQLAlchemy** - ORM 数据库访问
- **MySQL** - 关系型数据库
- **JWT** - 用户认证
- **MiniMax Image-01** - AI 图片生成服务

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Element Plus** - UI 组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Vite** - 快速的构建工具

## 项目结构

```
ootd-fastapi/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic 模型
│   │   └── services/    # 业务逻辑服务
│   ├── main.py          # 应用入口
│   ├── init_db.py       # 数据库初始化脚本
│   ├── requirements.txt # Python 依赖
│   └── .env.example     # 环境变量示例
│
└── frontend/            # Vue 3 前端
    ├── src/
    │   ├── api/        # API 客户端
    │   ├── router/     # 路由配置
    │   ├── stores/     # Pinia 状态
    │   ├── views/      # 页面组件
    │   └── main.ts     # 应用入口
    ├── package.json
    └── vite.config.ts
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- MySQL 5.7+

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和 API 密钥
```

5. 初始化数据库：
```bash
python init_db.py
```

6. 启动后端服务：
```bash
python main.py
# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端将运行在 http://localhost:8000

API 文档访问：http://localhost:8000/api/docs

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端将运行在 http://localhost:5173

## 环境变量配置

### 后端 (.env)

```env
# FastAPI Configuration
APP_NAME=穿搭AI
DEBUG=True
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ootd_fastapi

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_EXPIRE_MINUTES=10080

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# MiniMax AI
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_GROUP_ID=your-group-id

# Alibaba Cloud OSS (可选)
OSS_REGION=oss-cn-hangzhou
OSS_ACCESS_KEY_ID=your-oss-access-key-id
OSS_ACCESS_KEY_SECRET=your-oss-access-key-secret
OSS_BUCKET=your-bucket-name

# Upload
UPLOAD_DIR=/data/public/uploads
MAX_UPLOAD_SIZE=10485760
```

## 核心功能

### 用户功能
- 用户注册/登录
- 个人资料管理（身高、体重、体型、肤色）
- 头像上传

### 衣物管理
- 添加衣物（支持图片上传）
- 按分类/搜索筛选
- 查看衣物详情

### 穿搭管理
- AI 智能生成穿搭（使用 MiniMax Image-01）
- 手动创建 DIY 穿搭
- 查看穿搭记录

## API 端点

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出

### 用户
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息

### 衣物
- `GET /api/clothing` - 获取衣物列表
- `POST /api/clothing` - 添加衣物
- `GET /api/clothing/{id}` - 获取衣物详情
- `PUT /api/clothing/{id}` - 更新衣物
- `DELETE /api/clothing/{id}` - 删除衣物

### 穿搭
- `GET /api/outfits` - 获取穿搭列表
- `POST /api/outfits/create` - 创建 DIY 穿搭
- `POST /api/outfits/generate` - AI 生成穿搭
- `GET /api/outfits/{id}` - 获取穿搭详情
- `DELETE /api/outfits/{id}` - 删除穿搭

### 上传
- `POST /api/upload/image` - 上传图片
- `POST /api/upload/avatar` - 上传头像

## 部署

### 后端部署

```bash
# 设置生产环境变量
export FLASK_ENV=production

# 使用 gunicorn 启动
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 前端部署

```bash
# 构建生产版本
npm run build

# dist 目录可部署到 nginx 或其他静态文件服务器
```

## 开发说明

### 添加新的 API 端点

1. 在 `backend/app/api/` 创建路由文件
2. 在 `backend/app/schemas/` 添加请求/响应模型
3. 在 `backend/main.py` 注册路由

### 添加新的页面

1. 在 `frontend/src/views/` 创建页面组件
2. 在 `frontend/src/router/index.ts` 添加路由
3. 在侧边栏添加菜单项（如需要）

## 许可证

MIT
