# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OOTD (Outfit of the Day) 穿搭AI is a Chinese-language outfit recommendation application built with Next.js 16, React 19, and TypeScript. It helps users digitize their wardrobe and generate AI-powered outfit suggestions using Alibaba's Tongyi Wanxiang API.

## Common Commands

### Development
```bash
npm run dev          # Start development server (http://localhost:3000)
npm run build        # Build for production
npm start            # Start production server
npm run lint         # Run ESLint
```

### Database
```bash
npx prisma generate  # Generate Prisma Client (runs automatically on install)
npx prisma migrate dev        # Create and apply new migration
npx prisma migrate dev --name init  # Create initial migration
npx prisma studio             # Open Prisma Studio for database inspection
npx prisma db push            # Push schema changes to database (development only)
```

## Architecture

### Tech Stack
- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, TailwindCSS v4
- **Backend**: Next.js API Routes, NextAuth.js v4
- **Database**: Prisma ORM with MySQL
- **AI**: Alibaba Tongyi Wanxiang API (通义万相)
- **State**: Zustand for client state
- **Authentication**: NextAuth.js with Credentials provider (JWT sessions)

### Directory Structure

```
app/
├── (auth)/              # Auth route group (login, register)
├── dashboard/           # Protected dashboard pages
│   ├── wardrobe/        # Clothing management
│   ├── outfits/         # Outfit management (generate, diy, view)
│   └── profile/         # User profile with body characteristics
├── api/                 # API routes
│   ├── auth/           # NextAuth endpoints
│   ├── wardrobe/       # Clothing CRUD
│   ├── outfits/        # Outfit CRUD and AI generation
│   ├── upload/         # Image upload
│   └── user/           # User profile
├── layout.tsx          # Root layout
└── page.tsx            # Landing page

components/
├── ui/                 # shadcn/ui-style base components (button, card, dialog, etc.)
└── wardrobe/           # Feature-specific components

lib/
├── auth.ts             # NextAuth configuration
├── prisma.ts           # Prisma client singleton
├── tongyi.ts           # Tongyi Wanxiang API client
├── oss.ts              # Alibaba Cloud OSS client
├── upload.ts           # Image upload handling (OSS with local fallback)
└── utils.ts            # Utilities (cn, parseJsonArray, stringifyJsonArray)

prisma/
└── schema.prisma       # Database schema

types/
└── next-auth.d.ts      # NextAuth type extensions
```

### Data Models (Prisma)

- **User**: Account with body characteristics (height, weight, bodyType, skinTone)
- **Clothing**: Individual items with category, color, style, season, imageUrl
- **Outfit**: Saved outfit combinations with aiGenerated flag, reasoning, tips
- **OutfitItem**: Junction table linking outfits to clothing items

Note: Arrays (color, style, season) are stored as JSON strings in MySQL.

### Authentication Flow

1. All API routes use `getServerSession(authOptions)` to verify authentication
2. JWT strategy with custom callbacks to attach user.id to token/session
3. Custom login page at `/auth/login`
4. Session data includes: `{ user: { id, email, name } }`

### API Route Pattern

All API routes follow this pattern:
```typescript
export async function GET/POST/DELETE(req: Request) {
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }
    // ... business logic with Prisma
    return NextResponse.json(data)
  } catch (error) {
    console.error("Operation error:", error)
    return NextResponse.json({ error: "Error message" }, { status: 500 })
  }
}
```

### AI Integration (Tongyi Wanxiang)

Located in `lib/tongyi.ts`:
- Falls back to mock logic if `TONGYI_API_KEY` is not configured
- Accepts user characteristics, clothing items, and requirements
- Returns: `selected_items` (IDs), `reasoning` (string), `tips` (string[])
- Always returns valid response even on API failure

### Environment Variables

Required in `.env`:
```bash
DATABASE_URL="mysql://username:password@localhost:3306/ootd"
NEXTAUTH_SECRET="your-secret-key"
NEXTAUTH_URL="http://localhost:3000"
TONGYI_API_KEY="your-tongyi-api-key"

# Alibaba Cloud OSS (阿里云对象存储)
OSS_REGION="oss-cn-hangzhou"  # OSS region (e.g., oss-cn-hangzhou)
OSS_ACCESS_KEY_ID="your-oss-access-key-id"
OSS_ACCESS_KEY_SECRET="your-oss-access-key-secret"
OSS_BUCKET="your-bucket-name"

# Fallback local storage (used if OSS is not configured)
UPLOAD_DIR="/data/public/uploads"
```

### Path Alias

`@/*` maps to project root (configured in `tsconfig.json`)

### Component Styling

- TailwindCSS v4 with custom animations
- Components use CVA (class-variance-authority) for variants
- Utility function `cn()` merges clsx + tailwind-merge
- Follows shadcn/ui patterns for base components

### Important Patterns

1. **JSON Array Fields**: Use `parseJsonArray()` and `stringifyJsonArray()` from `lib/utils.ts` for database array fields
2. **Image Upload**: Handled via `lib/upload.ts` with Alibaba Cloud OSS (ali-oss SDK)
   - OSS configuration required: `OSS_REGION`, `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET`, `OSS_BUCKET`
   - Falls back to local storage if OSS is not configured
   - Files organized as: `uploads/YYYY/MM/uuid-filename`
   - Returns full public URL from OSS or relative path for local storage
3. **Authorization**: Always verify ownership before DELETE operations (check `userId === session.user.id`)
4. **Error Handling**: All API routes wrap in try-catch and return appropriate HTTP status codes
