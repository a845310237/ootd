import { getServerSession } from "next-auth"
import { redirect } from "next/navigation"
import { authOptions } from "@/lib/auth"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getServerSession(authOptions)

  if (!session) {
    redirect("/auth/login")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/dashboard" className="text-2xl font-bold text-blue-600">
            穿搭AI
          </Link>
          <nav className="hidden md:flex items-center space-x-6">
            <Link href="/dashboard/wardrobe" className="text-gray-700 hover:text-blue-600 transition">
              我的衣柜
            </Link>
            <Link href="/dashboard/outfits" className="text-gray-700 hover:text-blue-600 transition">
              穿搭方案
            </Link>
            <Link href="/dashboard/outfits/generate" className="text-gray-700 hover:text-blue-600 transition">
              AI搭配
            </Link>
            <Link href="/dashboard/profile" className="text-gray-700 hover:text-blue-600 transition">
              个人资料
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600 hidden sm:block">
              {session.user.email}
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                if (typeof window !== 'undefined') {
                  window.location.href = '/api/auth/signout'
                }
              }}
            >
              退出
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <nav className="md:hidden bg-white border-b px-4 py-2 flex justify-around">
        <Link href="/dashboard/wardrobe" className="text-sm text-gray-700">
          衣柜
        </Link>
        <Link href="/dashboard/outfits" className="text-sm text-gray-700">
          方案
        </Link>
        <Link href="/dashboard/outfits/generate" className="text-sm text-gray-700">
          AI搭配
        </Link>
        <Link href="/dashboard/profile" className="text-sm text-gray-700">
          我的
        </Link>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
