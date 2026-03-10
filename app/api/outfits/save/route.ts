import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { prisma } from "@/lib/prisma"

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const body = await req.json()
    const { name, style, occasion, season, selectedItems, reasoning, tips, aiGenerated } = body

    if (!name || !selectedItems || selectedItems.length === 0) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 }
      )
    }

    // Create outfit with items in a transaction
    const outfit = await prisma.$transaction(async (tx) => {
      // Create outfit
      const newOutfit = await tx.outfit.create({
        data: {
          userId: session.user.id,
          name,
          style,
          occasion,
          season,
          aiGenerated: aiGenerated || false,
          reasoning,
          tips: JSON.stringify(tips || []),
        },
      })

      // Create outfit items
      for (const clothingId of selectedItems) {
        await tx.outfitItem.create({
          data: {
            outfitId: newOutfit.id,
            clothingId,
          },
        })
      }

      return newOutfit
    })

    return NextResponse.json(outfit, { status: 201 })
  } catch (error) {
    console.error("Outfit save error:", error)
    return NextResponse.json(
      { error: "Failed to save outfit" },
      { status: 500 }
    )
  }
}
