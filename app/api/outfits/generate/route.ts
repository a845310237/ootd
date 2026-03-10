import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { prisma } from "@/lib/prisma"
import { generateOutfitRecommendation } from "@/lib/tongyi"

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await req.json()
    const { style, occasion, season } = body

    if (!style || !occasion || !season) {
      return NextResponse.json(
        { error: "Missing required parameters" },
        { status: 400 }
      )
    }

    // Get user info
    const user = await prisma.user.findUnique({
      where: { id: session.user.id },
      select: {
        id: true,
        height: true,
        weight: true,
        bodyType: true,
        skinTone: true,
      }
    })

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    // Get user's clothes
    const clothes = await prisma.clothing.findMany({
      where: { userId: session.user.id },
      select: {
        id: true,
        name: true,
        category: true,
        color: true,
        style: true,
        season: true,
        imageUrl: true,
      }
    })

    if (clothes.length === 0) {
      return NextResponse.json(
        { error: "请先添加衣物到衣柜" },
        { status: 400 }
      )
    }

    // Parse JSON fields
    const parsedClothes = clothes.map((c) => ({
      id: c.id,
      name: c.name,
      category: c.category,
      color: JSON.parse(c.color || "[]"),
      style: JSON.parse(c.style || "[]"),
      season: JSON.parse(c.season || "[]"),
      imageUrl: c.imageUrl,
    }))

    // Call AI API
    const recommendation = await generateOutfitRecommendation({
      user: {
        height: user.height || 170,
        weight: user.weight || 65,
        bodyType: user.bodyType || "标准",
        skinTone: user.skinTone || "中性",
      },
      clothes: parsedClothes,
      requirements: { style, occasion, season },
    })

    // Get selected clothing details
    const selectedClothes = parsedClothes.filter((c) =>
      recommendation.selected_items.includes(c.id)
    )

    return NextResponse.json({
      selected_items: selectedClothes,
      reasoning: recommendation.reasoning,
      tips: recommendation.tips,
      requirements: { style, occasion, season },
    })
  } catch (error) {
    console.error("Outfit generation error:", error)
    return NextResponse.json(
      { error: "Failed to generate outfit" },
      { status: 500 }
    )
  }
}
