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
- **Next.js 16** - React 框架，支持 SSR 和 App Router
- **React 19** - UI 库
- **TypeScript** - 类型安全
- **TailwindCSS** - 样式框架

### UI 组件
- **Lucide React** - 图标库
- **React Dropzone** - 文件上传
- **Class Variance Authority** - 组件样式变体管理

### 后端服务
- **NextAuth.js** - 身份认证
- **Prisma** - ORM 数据库访问
- **MySQL** - 数据库

### AI 集成
- **阿里通义万相 API** - AI 穿搭推荐生成

### 状态管理
- **Zustand** - 轻量级状态管理

### 工具库
- **bcryptjs** - 密码加密
- **clsx / tailwind-merge** - 样式类名管理

## 项目结构

```
ootd/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # 认证相关页面组
│   │   ├── login/               # 登录页面
│   │   └── register/            # 注册页面
│   ├── dashboard/               # 用户仪表板
│   │   ├── wardrobe/            # 衣物管理
│   │   │   ├── add/            # 添加衣物
│   │   │   └── page.tsx        # 衣物列表
│   │   ├── outfits/            # 穿搭管理
│   │   │   ├── generate/       # AI 生成穿搭
│   │   │   ├── diy/            # DIY 穿搭
│   │   │   └── [id]/           # 穿搭详情
│   │   ├── profile/            # 个人资料
│   │   └── page.tsx            # 仪表板首页
│   ├── api/                     # API 路由
│   │   ├── auth/               # 认证 API
│   │   ├── wardrobe/           # 衣物 API
│   │   ├── outfits/            # 穿搭 API
│   │   ├── upload/             # 图片上传
│   │   └── user/               # 用户 API
│   ├── layout.tsx              # 根布局
│   └── page.tsx                # 首页
├── components/                   # React 组件
│   ├── ui/                     # 基础 UI 组件
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── form.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   ├── select.tsx
│   │   └── badge.tsx
│   ├── wardrobe/               # 衣物相关组件
│   │   └── clothing-card.tsx
│   └── outfits/                # 穿搭相关组件
├── lib/                         # 工具函数和配置
│   ├── auth.ts                 # NextAuth 配置
│   ├── prisma.ts               # Prisma 客户端
│   ├── tongyi.ts               # 通义万相 API
│   ├── upload.ts               # 文件上传处理
│   └── utils.ts                # 通用工具函数
├── prisma/                      # Prisma 配置
│   └── schema.prisma           # 数据库模型
├── types/                       # TypeScript 类型定义
│   └── next-auth.d.ts          # NextAuth 类型扩展
├── public/                      # 静态资源
│   └── uploads/                # 用户上传图片
├── next.config.js              # Next.js 配置
├── tailwind.config.ts          # TailwindCSS 配置
├── tsconfig.json               # TypeScript 配置
└── package.json                # 项目依赖
```

## 数据模型

### User（用户）
- 用户账户和基本信息
- 身材特征（身高、体重、体型、肤色）

### Clothing（衣物）
- 单品信息（名称、分类、颜色、风格）
- 品牌、尺码、材质
- 季节适用性
- 关联图片

### Outfit（穿搭）
- 穿搭组合名称和风格
- 适用场合和季节
- AI 生成标识
- 搭配理由和小贴士
- AI 生成的效果图

### OutfitItem（穿搭单品）
- Outfit 和 Clothing 的关联表
- 记录穿搭中使用的单品

## 环境配置

复制 `.env.example` 到 `.env` 并配置以下变量：

```env
# MySQL 数据库连接
DATABASE_URL="mysql://username:password@localhost:3306/ootd"

# NextAuth 认证
NEXTAUTH_SECRET="your-secret-key-here-change-this-in-production"
NEXTAUTH_URL="http://localhost:3000"

# 阿里通义万相 API
TONGYI_API_KEY="your-tongyi-api-key"

# 图片存储路径（本地）
UPLOAD_DIR="/data/public/uploads"
```

## 安装和运行

### 安装依赖

```bash
npm install
```

### 初始化数据库

```bash
# 生成 Prisma Client
npx prisma generate

# 运行数据库迁移
npx prisma migrate dev
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 生产构建

```bash
# 构建
npm run build

# 启动生产服务器
npm start
```

## API 路由

### 认证 API
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/signout` - 用户登出
- `GET/POST /api/auth/[...nextauth]` - NextAuth 会话管理

### 用户 API
- `GET/PUT /api/user/profile` - 获取/更新用户资料

### 衣物 API
- `GET /api/wardrobe` - 获取衣物列表
- `POST /api/wardrobe` - 添加衣物
- `DELETE /api/wardrobe` - 删除衣物

### 穿搭 API
- `GET /api/outfits` - 获取穿搭列表
- `POST /api/outfits/create` - 创建 DIY 穿搭
- `POST /api/outfits/generate` - AI 生成穿搭
- `POST /api/outfits/save` - 保存 AI 生成的穿搭
- `GET/DELETE /api/outfits/[id]` - 获取/删除穿搭详情

### 上传 API
- `POST /api/upload` - 上传图片

## AI 功能说明

### 通义万相集成

应用集成了阿里云通义万相 API，根据以下信息生成穿搭建议：

1. **用户特征**：身高、体重、体型、肤色
2. **可用衣物**：用户衣柜中的所有单品
3. **穿搭需求**：风格、场合、季节

### 返回结果

- `selected_items`：选中的衣物 ID 列表
- `reasoning`：详细的搭配理由
- `tips`：穿搭小贴士数组

当 API 未配置或调用失败时，系统会使用本地模拟逻辑返回推荐结果。

## 主要页面

### 首页
- 展示应用核心功能
- 快速导航入口

### 登录/注册
- 用户身份认证
- NextAuth.js 集成

### 仪表板
- **衣柜管理**：查看、添加、删除衣物
- **穿搭生成**：AI 智能生成穿搭
- **DIY 穿搭**：手动创建穿搭组合
- **穿搭记录**：查看历史穿搭
- **个人资料**：管理身材特征信息

## 开发说明

### 代码规范
- 使用 TypeScript 进行类型检查
- 遵循 ESLint 规则
- 使用 TailwindCSS 进行样式开发

### 组件开发
- 使用 shadcn/ui 风格的基础组件
- 通过 Class Variance Authority 管理组件变体
- 使用 clsx 和 tailwind-merge 合并类名

### 数据库操作
- 使用 Prisma Client 进行数据访问
- 所有数据库操作在 API 路由中进行
- 使用 Prisma Middleware 处理数据格式化

## 依赖版本

主要依赖版本信息详见 `package.json`

## 许可证

ISC
