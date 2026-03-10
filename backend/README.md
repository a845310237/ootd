# OOTD Backend - FastAPI Full-Stack Application

穿搭AI（Outfit of the Day）后端应用，使用 FastAPI + Jinja2 + SQLAlchemy + MySQL 构建。

## 功能特性

- 🔐 **用户认证**：JWT Token 认证系统
- 👔 **智能衣柜**：衣物管理、分类、搜索
- ✨ **AI 穿搭推荐**：集成通义万相 API
- 👗 **穿搭管理**：DIY 穿搭、AI 生成穿搭
- 📝 **个人资料**：身材特征、肤色等信息管理
- 📤 **图片上传**：支持衣物图片上传

## 技术栈

- **框架**：FastAPI 0.104+
- **模板引擎**：Jinja2 3.1+
- **ORM**：SQLAlchemy 2.0+
- **数据库**：MySQL
- **认证**：JWT (python-jose)
- **密码加密**：bcrypt
- **HTTP 客户端**：httpx
- **ASGI 服务器**：Uvicorn

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── api/
│   │   └── v1/                 # API 路由
│   ├── core/                   # 核心配置
│   ├── models/                 # SQLAlchemy 模型
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # 业务逻辑
│   ├── templates/              # Jinja2 模板
│   ├── static/                 # 静态文件
│   └── utils/                  # 工具函数
├── requirements.txt            # Python 依赖
├── .env                        # 环境变量
└── pyproject.toml             # 项目配置
```

## 安装和运行

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 应用配置
APP_NAME=穿搭AI
DEBUG=True
SECRET_KEY=your-secret-key-change-this

# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ootd

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# 通义万相 API（可选）
TONGYI_API_KEY=your-tongyi-api-key-here
```

### 3. 运行应用

```bash
# 开发模式（自动重载）
python -m app.main

# 或使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

应用将在 `http://localhost:8000` 启动。

### 4. 访问应用

- **首页**：http://localhost:8000/
- **API 文档**：http://localhost:8000/api/docs
- **仪表板**：http://localhost:8000/dashboard（需要登录）

## API 端点

### 认证

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/logout` - 用户登出

### 用户

- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新当前用户信息

### 衣柜

- `GET /api/v1/wardrobe` - 获取衣物列表
- `POST /api/v1/wardrobe` - 添加衣物
- `PUT /api/v1/wardrobe/{id}` - 更新衣物
- `DELETE /api/v1/wardrobe/{id}` - 删除衣物
- `GET /api/v1/wardrobe/categories` - 获取分类列表

### 穿搭

- `GET /api/v1/outfits` - 获取穿搭列表
- `POST /api/v1/outfits` - 创建 DIY 穿搭
- `POST /api/v1/outfits/generate` - AI 生成穿搭
- `GET /api/v1/outfits/{id}` - 获取穿搭详情
- `PUT /api/v1/outfits/{id}` - 更新穿搭
- `DELETE /api/v1/outfits/{id}` - 删除穿搭

### 上传

- `POST /api/v1/upload` - 上传图片

## 开发

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black app/
```

### 代码检查

```bash
ruff check app/
```

## 数据库模型

### User（用户）
- id: 用户唯一标识
- email: 邮箱（唯一）
- password: 密码（哈希）
- name: 昵称
- height: 身高（cm）
- weight: 体重（kg）
- body_type: 体型
- skin_tone: 肤色
- avatar: 头像 URL

### Clothing（衣物）
- id: 衣物唯一标识
- user_id: 所属用户
- name: 名称
- category: 分类
- color: 颜色（JSON）
- style: 风格（JSON）
- season: 季节（JSON）
- brand: 品牌
- size: 尺码
- material: 材质
- image_url: 图片 URL

### Outfit（穿搭）
- id: 穿搭唯一标识
- user_id: 所属用户
- name: 名称
- style: 风格
- occasion: 场合
- season: 季节
- ai_generated: 是否 AI 生成
- result_url: 生成结果图
- reasoning: 搭配理由
- tips: 穿搭小贴士（JSON）

## 部署

### 生产环境配置

1. 设置环境变量：
   ```env
   DEBUG=False
   SECRET_KEY=强密码
   JWT_SECRET_KEY=强JWT密钥
   ```

2. 使用生产级 ASGI 服务器：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

3. 配置反向代理（如 Nginx）

4. 设置 HTTPS

## 许可证

MIT License
