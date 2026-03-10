"use client"

import { useState, useEffect } from "react"
import { ClothingCard } from "@/components/wardrobe/clothing-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select } from "@/components/ui/select"
import Link from "next/link"
import { Plus, Search } from "lucide-react"

export default function WardrobePage() {
  const [clothes, setClothes] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [categoryFilter, setCategoryFilter] = useState("all")
  const [searchQuery, setSearchQuery] = useState("")

  useEffect(() => {
    fetchClothes()
  }, [categoryFilter, searchQuery])

  const fetchClothes = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (categoryFilter !== "all") params.append("category", categoryFilter)
      if (searchQuery) params.append("search", searchQuery)

      const response = await fetch(`/api/wardrobe?${params}`)
      const data = await response.json()
      setClothes(data)
    } catch (error) {
      console.error("Failed to fetch clothes:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = (id: string) => {
    setClothes(clothes.filter((item) => item.id !== id))
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">我的衣柜</h1>
          <p className="text-gray-600 mt-1">
            共 {clothes.length} 件衣物
          </p>
        </div>
        <Link href="/dashboard/wardrobe/add">
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            添加衣物
          </Button>
        </Link>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="搜索衣物..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
          className="flex h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
        >
          <option value="all">全部分类</option>
          <option value="上衣">上衣</option>
          <option value="裤子">裤子</option>
          <option value="鞋子">鞋子</option>
          <option value="外套">外套</option>
          <option value="裙子">裙子</option>
          <option value="配饰">配饰</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">
          加载中...
        </div>
      ) : clothes.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">
            {searchQuery || categoryFilter !== "all"
              ? "没有找到匹配的衣物"
              : "您的衣柜还是空的"}
          </p>
          {!searchQuery && categoryFilter === "all" && (
            <Link href="/dashboard/wardrobe/add">
              <Button>添加第一件衣物</Button>
            </Link>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {clothes.map((item) => (
            <ClothingCard
              key={item.id}
              {...item}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}
