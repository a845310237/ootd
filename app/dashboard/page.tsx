import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { getServerSession } from "next-auth"
import { authOptions } from "@/lib/auth"
import { prisma } from "@/lib/prisma"

export default async function DashboardPage() {
  const session = await getServerSession(authOptions)

  // Get user's clothing count and outfit count
  const [clothingCount, outfitCount] = await Promise.all([
    prisma.clothing.count({
      where: { userId: session.user.id }
    }),
    prisma.outfit.count({
      where: { userId: session.user.id }
    })
  ])

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          欢迎回来，{session.user.name || session.user.email}！
        </h1>
        <p className="text-gray-600 mt-2">
          开始管理您的衣柜，让AI为您打造专属穿搭
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>我的衣物</CardDescription>
            <CardTitle className="text-3xl">{clothingCount}</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/dashboard/wardrobe">
              <Button variant="outline" className="w-full">
                查看衣柜
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>穿搭方案</CardDescription>
            <CardTitle className="text-3xl">{outfitCount}</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/dashboard/outfits">
              <Button variant="outline" className="w-full">
                查看方案
              </Button>
            </Link>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>快速开始</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Link href="/dashboard/wardrobe/add">
              <Button className="w-full justify-start" variant="outline">
                ➕ 添加新衣物
              </Button>
            </Link>
            <Link href="/dashboard/outfits/generate">
              <Button className="w-full justify-start" variant="outline">
                🤖 AI智能搭配
              </Button>
            </Link>
            <Link href="/dashboard/outfits/diy">
              <Button className="w-full justify-start" variant="outline">
                ✨ DIY穿搭
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>

      {clothingCount === 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle>开始您的穿搭之旅</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 mb-4">
              您还没有添加任何衣物。开始添加您的衣物，让AI为您提供个性化穿搭建议吧！
            </p>
            <Link href="/dashboard/wardrobe/add">
              <Button>添加第一件衣物</Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
