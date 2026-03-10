"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Image from "next/image"
import { Trash2, Eye } from "lucide-react"

export default function OutfitsPage() {
  const [outfits, setOutfits] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")

  useEffect(() => {
    fetchOutfits()
  }, [])

  const fetchOutfits = async () => {
    setLoading(true)
    try {
      const response = await fetch("/api/outfits")
      const data = await response.json()
      setOutfits(data)
    } catch (error) {
      console.error("Failed to fetch outfits:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm("确定要删除这个穿搭方案吗？")) return

    try {
      const response = await fetch(`/api/outfits/${id}`, {
        method: "DELETE",
      })

      if (response.ok) {
        setOutfits(outfits.filter((o) => o.id !== id))
      }
    } catch (error) {
      console.error("Delete error:", error)
      alert("删除失败")
    }
  }

  const filteredOutfits = outfits.filter((o) =>
    o.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (o.style && o.style.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">我的穿搭方案</h1>
          <p className="text-gray-600 mt-1">
            共 {outfits.length} 个方案
          </p>
        </div>
        <div className="flex gap-2">
          <Link href="/dashboard/outfits/generate">
            <Button variant="outline">AI搭配</Button>
          </Link>
          <Link href="/dashboard/outfits/diy">
            <Button>DIY穿搭</Button>
          </Link>
        </div>
      </div>

      <div className="relative">
        <Input
          placeholder="搜索穿搭方案..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">加载中...</div>
      ) : filteredOutfits.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">
            {searchQuery ? "没有找到匹配的方案" : "还没有穿搭方案"}
          </p>
          {!searchQuery && (
            <div className="flex gap-2 justify-center">
              <Link href="/dashboard/outfits/generate">
                <Button variant="outline">AI搭配</Button>
              </Link>
              <Link href="/dashboard/outfits/diy">
                <Button>DIY穿搭</Button>
              </Link>
            </div>
          )}
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredOutfits.map((outfit) => (
            <Card key={outfit.id} className="overflow-hidden">
              <div className="grid grid-cols-3 gap-1 p-2 bg-gray-50">
                {outfit.items.slice(0, 6).map((item: any) => (
                  <div key={item.id} className="relative aspect-square bg-gray-100 rounded">
                    <Image
                      src={item.clothing.imageUrl || "/placeholder-clothing.jpg"}
                      alt={item.clothing.name}
                      fill
                      className="object-cover"
                      sizes="100px"
                    />
                  </div>
                ))}
                {outfit.items.length > 6 && (
                  <div className="relative aspect-square bg-gray-100 rounded flex items-center justify-center text-gray-500 text-sm">
                    +{outfit.items.length - 6}
                  </div>
                )}
              </div>
              <CardContent className="p-4">
                <h3 className="font-semibold text-lg mb-1">{outfit.name}</h3>
                <div className="flex flex-wrap gap-1 mb-3">
                  {outfit.style && (
                    <Badge variant="secondary" className="text-xs">
                      {outfit.style}
                    </Badge>
                  )}
                  {outfit.occasion && (
                    <Badge variant="outline" className="text-xs">
                      {outfit.occasion}
                    </Badge>
                  )}
                  {outfit.season && (
                    <Badge variant="outline" className="text-xs">
                      {outfit.season}
                    </Badge>
                  )}
                  {outfit.aiGenerated && (
                    <Badge variant="default" className="text-xs">
                      AI
                    </Badge>
                  )}
                </div>
                <div className="flex gap-2">
                  <Link href={`/dashboard/outfits/${outfit.id}`} className="flex-1">
                    <Button variant="outline" size="sm" className="w-full">
                      <Eye className="h-3 w-3 mr-1" />
                      查看
                    </Button>
                  </Link>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDelete(outfit.id)}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
