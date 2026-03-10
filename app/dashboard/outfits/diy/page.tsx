"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"
import { Plus, X } from "lucide-react"

const CATEGORIES = ["上衣", "裤子", "鞋子", "外套", "裙子", "配饰"]

export default function DIYOutfitPage() {
  const router = useRouter()
  const [clothes, setClothes] = useState<any[]>([])
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [outfitName, setOutfitName] = useState("")
  const [style, setStyle] = useState("")
  const [occasion, setOccasion] = useState("")
  const [season, setSeason] = useState("")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    fetchClothes()
  }, [])

  const fetchClothes = async () => {
    try {
      const response = await fetch("/api/wardrobe")
      const data = await response.json()
      setClothes(data)
    } catch (error) {
      console.error("Failed to fetch clothes:", error)
    } finally {
      setLoading(false)
    }
  }

  const toggleSelection = (id: string) => {
    const newSelected = new Set(selectedIds)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelectedIds(newSelected)
  }

  const handleSave = async () => {
    if (selectedIds.size === 0) {
      alert("请至少选择一件衣物")
      return
    }

    if (!outfitName.trim()) {
      alert("请输入穿搭方案名称")
      return
    }

    setSaving(true)

    try {
      const response = await fetch("/api/outfits/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: outfitName,
          style,
          occasion,
          season,
          selectedItems: Array.from(selectedIds),
        }),
      })

      if (response.ok) {
        router.push("/dashboard/outfits")
      } else {
        throw new Error("保存失败")
      }
    } catch (error) {
      alert("保存失败，请稍后重试")
    } finally {
      setSaving(false)
    }
  }

  const filteredClothes = selectedCategory === "all"
    ? clothes
    : clothes.filter((c) => c.category === selectedCategory)

  const selectedClothes = clothes.filter((c) => selectedIds.has(c.id))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">DIY穿搭</h1>
        <p className="text-gray-600 mt-1">
          从衣柜中选择衣物，创建属于您的穿搭方案
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Clothes Selection */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>选择衣物</CardTitle>
              <CardDescription>点击选择要搭配的衣物</CardDescription>
            </CardHeader>
            <CardContent>
              {/* Category Filter */}
              <div className="flex flex-wrap gap-2 mb-4">
                <button
                  onClick={() => setSelectedCategory("all")}
                  className={`px-3 py-1 rounded-full text-sm ${
                    selectedCategory === "all"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700"
                  }`}
                >
                  全部
                </button>
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-3 py-1 rounded-full text-sm ${
                      selectedCategory === cat
                        ? "bg-blue-600 text-white"
                        : "bg-gray-100 text-gray-700"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>

              {loading ? (
                <div className="text-center py-8 text-gray-500">
                  加载中...
                </div>
              ) : filteredClothes.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  该分类下没有衣物
                </div>
              ) : (
                <div className="grid grid-cols-3 gap-3">
                  {filteredClothes.map((item) => (
                    <div
                      key={item.id}
                      onClick={() => toggleSelection(item.id)}
                      className={`relative aspect-square rounded-lg overflow-hidden cursor-pointer border-2 transition ${
                        selectedIds.has(item.id)
                          ? "border-blue-600 ring-2 ring-blue-200"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <Image
                        src={item.imageUrl || "/placeholder-clothing.jpg"}
                        alt={item.name}
                        fill
                        className="object-cover"
                        sizes="(max-width: 768px) 33vw, 25vw"
                      />
                      {selectedIds.has(item.id) && (
                        <div className="absolute top-1 right-1 bg-blue-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                          ✓
                        </div>
                      )}
                      <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white p-1 text-xs truncate">
                        {item.name}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Selected Items & Form */}
        <div className="space-y-4">
          <Card className="sticky top-4">
            <CardHeader>
              <CardTitle>已选衣物</CardTitle>
              <CardDescription>
                已选择 {selectedIds.size} 件
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Selected Items Preview */}
              {selectedClothes.length > 0 ? (
                <div className="grid grid-cols-3 gap-2">
                  {selectedClothes.map((item) => (
                    <div
                      key={item.id}
                      className="relative aspect-square rounded-lg overflow-hidden"
                    >
                      <Image
                        src={item.imageUrl || "/placeholder-clothing.jpg"}
                        alt={item.name}
                        fill
                        className="object-cover"
                        sizes="100px"
                      />
                      <button
                        onClick={() => toggleSelection(item.id)}
                        className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs hover:bg-red-600"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-400 text-sm">
                  还没有选择衣物
                </div>
              )}

              {/* Outfit Details Form */}
              <div className="space-y-3 pt-4 border-t">
                <div>
                  <Label htmlFor="outfitName">方案名称 *</Label>
                  <Input
                    id="outfitName"
                    value={outfitName}
                    onChange={(e) => setOutfitName(e.target.value)}
                    placeholder="我的穿搭方案"
                  />
                </div>
                <div>
                  <Label htmlFor="style">风格</Label>
                  <Input
                    id="style"
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    placeholder="如：休闲、正式"
                  />
                </div>
                <div>
                  <Label htmlFor="occasion">场合</Label>
                  <Input
                    id="occasion"
                    value={occasion}
                    onChange={(e) => setOccasion(e.target.value)}
                    placeholder="如：日常、工作"
                  />
                </div>
                <div>
                  <Label htmlFor="season">季节</Label>
                  <Input
                    id="season"
                    value={season}
                    onChange={(e) => setSeason(e.target.value)}
                    placeholder="如：春、夏"
                  />
                </div>
              </div>

              <Button
                onClick={handleSave}
                disabled={saving || selectedIds.size === 0}
                className="w-full"
              >
                {saving ? "保存中..." : "保存穿搭方案"}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
