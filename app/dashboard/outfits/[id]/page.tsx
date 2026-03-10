"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Image as ImageIcon, Trash2, Edit } from "lucide-react"
import Image from "next/image"

export default function OutfitDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()
  const [outfit, setOutfit] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOutfit()
  }, [params.id])

  const fetchOutfit = async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/outfits/${params.id}`)
      const data = await response.json()
      setOutfit(data)
    } catch (error) {
      console.error("Failed to fetch outfit:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm("确定要删除这个穿搭方案吗？")) return

    try {
      const response = await fetch(`/api/outfits/${params.id}`, {
        method: "DELETE",
      })

      if (response.ok) {
        router.push("/dashboard/outfits")
      }
    } catch (error) {
      console.error("Delete error:", error)
      alert("删除失败")
    }
  }

  if (loading) {
    return (
      <div className="text-center py-12 text-gray-500">
        加载中...
      </div>
    )
  }

  if (!outfit) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 mb-4">穿搭方案不存在</p>
        <Link href="/dashboard/outfits">
          <Button>返回方案列表</Button>
        </Link>
      </div>
    )
  }

  const tips = outfit.tips ? JSON.parse(outfit.tips) : []

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{outfit.name}</h1>
          <div className="flex flex-wrap gap-2 mt-2">
            {outfit.style && (
              <Badge variant="secondary">{outfit.style}</Badge>
            )}
            {outfit.occasion && (
              <Badge variant="outline">{outfit.occasion}</Badge>
            )}
            {outfit.season && (
              <Badge variant="outline">{outfit.season}</Badge>
            )}
            {outfit.aiGenerated && (
              <Badge>AI生成</Badge>
            )}
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleDelete}>
            <Trash2 className="h-4 w-4 mr-2" />
            删除
          </Button>
        </div>
      </div>

      {/* Clothing Items */}
      <Card>
        <CardHeader>
          <CardTitle>搭配单品</CardTitle>
          <CardDescription>
            共 {outfit.items.length} 件
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {outfit.items.map((item: any) => {
              const clothing = item.clothing
              const colors = clothing.color ? JSON.parse(clothing.color) : []
              return (
                <div key={item.id} className="space-y-2">
                  <div className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <Image
                      src={clothing.imageUrl || "/placeholder-clothing.jpg"}
                      alt={clothing.name}
                      fill
                      className="object-cover"
                      sizes="(max-width: 768px) 50vw, 25vw"
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-sm">{clothing.name}</h3>
                    <p className="text-xs text-gray-500">{clothing.category}</p>
                    {colors.length > 0 && (
                      <div className="flex gap-1 mt-1">
                        {colors.slice(0, 2).map((color: string, i: number) => (
                          <Badge key={i} variant="outline" className="text-xs">
                            {color}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* AI Reasoning and Tips (if available) */}
      {outfit.reasoning && (
        <Card>
          <CardHeader>
            <CardTitle>搭配说明</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700">{outfit.reasoning}</p>
          </CardContent>
        </Card>
      )}

      {tips.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>穿搭小贴士</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {tips.map((tip: string, index: number) => (
                <li key={index} className="flex items-start gap-2 text-gray-700">
                  <span className="text-blue-600 mt-1">•</span>
                  {tip}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Back Button */}
      <div>
        <Link href="/dashboard/outfits">
          <Button variant="outline">返回方案列表</Button>
        </Link>
      </div>
    </div>
  )
}
