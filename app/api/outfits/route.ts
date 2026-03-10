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

    const outfits = await prisma.outfit.findMany({
      where: { userId: session.user.id },
      include: {
        items: {
          include: {
            clothing: true,
          },
        },
      },
      orderBy: { createdAt: "desc" },
    })

    return NextResponse.json(outfits)
  } catch (error) {
    console.error("Outfits fetch error:", error)
    return NextResponse.json(
      { error: "Failed to fetch outfits" },
      { status: 500 }
    )
  }
}
