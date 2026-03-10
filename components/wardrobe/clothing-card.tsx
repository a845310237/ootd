"use client"

import Image from "next/image"
import Link from "next/link"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"
import { parseJsonArray } from "@/lib/utils"

interface ClothingCardProps {
  id: string
  name: string
  category: string
  color: string
  style: string
  season: string
  imageUrl: string
  brand?: string | null
  onDelete?: (id: string) => void
}

const CATEGORY_LABELS: Record<string, string> = {
  "上衣": "上衣",
  "裤子": "裤子",
  "鞋子": "鞋子",
  "配饰": "配饰",
  "外套": "外套",
  "裙子": "裙子",
  "内衣": "内衣",
}

export function ClothingCard({
  id,
  name,
  category,
  color,
  style,
  season,
  imageUrl,
  brand,
  onDelete,
}: ClothingCardProps) {
  const colors = parseJsonArray(color, [])
  const styles = parseJsonArray(style, [])
  const seasons = parseJsonArray(season, [])

  const handleDelete = async () => {
    if (!confirm("确定要删除这件衣物吗？")) return

    try {
      const response = await fetch(`/api/wardrobe?id=${id}`, {
        method: "DELETE",
      })

      if (response.ok && onDelete) {
        onDelete(id)
      }
    } catch (error) {
      console.error("Delete error:", error)
      alert("删除失败，请稍后重试")
    }
  }

  return (
    <Card className="overflow-hidden group">
      <div className="relative aspect-square bg-gray-100">
        <Image
          src={imageUrl || "/placeholder-clothing.jpg"}
          alt={name}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button
            size="icon"
            variant="destructive"
            onClick={handleDelete}
            className="h-8 w-8"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg mb-1">{name}</h3>
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <Badge variant="outline">{CATEGORY_LABELS[category] || category}</Badge>
          {brand && <span>{brand}</span>}
        </div>
        <div className="flex flex-wrap gap-1">
          {colors.slice(0, 2).map((c, i) => (
            <Badge key={i} variant="secondary" className="text-xs">
              {c}
            </Badge>
          ))}
          {styles.slice(0, 1).map((s, i) => (
            <Badge key={i} variant="secondary" className="text-xs">
              {s}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
