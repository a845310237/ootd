import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { prisma } from "@/lib/prisma"

export async function GET(req: Request) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const category = searchParams.get("category")
    const search = searchParams.get("search")

    const where: any = { userId: session.user.id }

    if (category && category !== "all") {
      where.category = category
    }

    if (search) {
      where.name = { contains: search }
    }

    const clothes = await prisma.clothing.findMany({
      where,
      orderBy: { createdAt: "desc" },
    })

    return NextResponse.json(clothes)
  } catch (error) {
    console.error("Wardrobe fetch error:", error)
    return NextResponse.json(
      { error: "Failed to fetch wardrobe" },
      { status: 500 }
    )
  }
}

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await req.json()
    const { name, category, color, style, season, brand, size, material, imageUrl } = body

    const clothing = await prisma.clothing.create({
      data: {
        userId: session.user.id,
        name,
        category,
        color: JSON.stringify(color || []),
        style: JSON.stringify(style || []),
        season: JSON.stringify(season || []),
        brand,
        size,
        material,
        imageUrl,
      },
    })

    return NextResponse.json(clothing, { status: 201 })
  } catch (error) {
    console.error("Clothing creation error:", error)
    return NextResponse.json(
      { error: "Failed to create clothing" },
      { status: 500 }
    )
  }
}

export async function DELETE(req: Request) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const { searchParams } = new URL(req.url)
    const id = searchParams.get("id")

    if (!id) {
      return NextResponse.json({ error: "Clothing ID required" }, { status: 400 })
    }

    // Verify ownership
    const clothing = await prisma.clothing.findUnique({
      where: { id },
    })

    if (!clothing || clothing.userId !== session.user.id) {
      return NextResponse.json({ error: "Clothing not found" }, { status: 404 })
    }

    await prisma.clothing.delete({
      where: { id },
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Clothing deletion error:", error)
    return NextResponse.json(
      { error: "Failed to delete clothing" },
      { status: 500 }
    )
  }
}
