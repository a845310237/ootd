import { NextResponse } from "next/server"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { prisma } from "@/lib/prisma"

export async function GET(
  req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    const outfit = await prisma.outfit.findUnique({
      where: { id: params.id },
      include: {
        items: {
          include: {
            clothing: true,
          },
        },
      },
    })

    if (!outfit || outfit.userId !== session.user.id) {
      return NextResponse.json({ error: "Outfit not found" }, { status: 404 })
    }

    return NextResponse.json(outfit)
  } catch (error) {
    console.error("Outfit fetch error:", error)
    return NextResponse.json(
      { error: "Failed to fetch outfit" },
      { status: 500 }
    )
  }
}

export async function DELETE(
  req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const session = await getServerSession(authOptions)

    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
    }

    // Verify ownership
    const outfit = await prisma.outfit.findUnique({
      where: { id: params.id },
    })

    if (!outfit || outfit.userId !== session.user.id) {
      return NextResponse.json({ error: "Outfit not found" }, { status: 404 })
    }

    await prisma.outfit.delete({
      where: { id: params.id },
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Outfit deletion error:", error)
    return NextResponse.json(
      { error: "Failed to delete outfit" },
      { status: 500 }
    )
  }
}
