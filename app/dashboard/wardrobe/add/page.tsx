"use client"

import { useState, useCallback } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Upload, X } from "lucide-react"
import Image from "next/image"

const CATEGORIES = ["上衣", "裤子", "鞋子", "外套", "裙子", "配饰", "内衣"]
const COLORS = ["黑色", "白色", "灰色", "红色", "蓝色", "绿色", "黄色", "粉色", "紫色", "棕色", "卡其色", "橙色", "米色"]
const STYLES = ["休闲", "正式", "运动", "复古", "简约", "时尚", "街头", "商务", "甜美", "酷帅"]
const SEASONS = ["春", "夏", "秋", "冬"]

export default function AddClothingPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: "",
    category: "上衣",
    color: [] as string[],
    style: [] as string[],
    season: [] as string[],
    brand: "",
    size: "",
    material: "",
  })
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  const toggleSelection = (array: string[], value: string) => {
    return array.includes(value)
      ? array.filter((item) => item !== value)
      : [...array, value]
  }

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith("image/")) {
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
    }
  }

  const handleUpload = async () => {
    if (!imageFile) {
      setError("请上传衣物照片")
      return null
    }

    setUploading(true)
    setError("")

    try {
      const formData = new FormData()
      formData.append("file", imageFile)

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "上传失败")
      }

      return data.url
    } catch (err) {
      setError(err instanceof Error ? err.message : "上传失败")
      return null
    } finally {
      setUploading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!formData.name.trim()) {
      setError("请输入衣物名称")
      return
    }

    if (!imagePreview) {
      setError("请上传衣物照片")
      return
    }

    setSaving(true)

    try {
      // Upload image first if not already uploaded
      let imageUrl = imagePreview
      if (imageFile && imageUrl.startsWith("blob:")) {
        imageUrl = await handleUpload() || ""
        if (!imageUrl) {
          setSaving(false)
          return
        }
      }

      const response = await fetch("/api/wardrobe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...formData,
          imageUrl,
        }),
      })

      if (!response.ok) {
        throw new Error("保存失败")
      }

      router.push("/dashboard/wardrobe")
    } catch (err) {
      setError(err instanceof Error ? err.message : "保存失败")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>添加衣物</CardTitle>
          <CardDescription>
            添加新衣物到您的衣柜
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            {/* Image Upload */}
            <div className="space-y-2">
              <Label>衣物照片 *</Label>
              <div
                onDrop={handleDrop}
                onDragOver={(e) => e.preventDefault()}
                className="relative border-2 border-dashed rounded-lg p-6 text-center hover:bg-gray-50 transition"
              >
                {imagePreview ? (
                  <div className="relative aspect-square max-w-xs mx-auto">
                    <Image
                      src={imagePreview}
                      alt="Preview"
                      fill
                      className="object-contain rounded"
                    />
                    <button
                      type="button"
                      onClick={() => {
                        setImageFile(null)
                        setImagePreview(null)
                      }}
                      className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div>
                    <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                    <p className="text-gray-600 mb-2">拖拽图片到这里，或点击选择</p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 cursor-pointer"
                    >
                      选择文件
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Name */}
            <div className="space-y-2">
              <Label htmlFor="name">衣物名称 *</Label>
              <Input
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="例如：白色T恤"
                required
              />
            </div>

            {/* Category */}
            <div className="space-y-2">
              <Label>分类 *</Label>
              <select
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>

            {/* Colors */}
            <div className="space-y-2">
              <Label>颜色（可多选）</Label>
              <div className="flex flex-wrap gap-2">
                {COLORS.map((color) => (
                  <button
                    key={color}
                    type="button"
                    onClick={() =>
                      setFormData({
                        ...formData,
                        color: toggleSelection(formData.color, color),
                      })
                    }
                    className={`px-3 py-1 rounded-full text-sm border-2 transition ${
                      formData.color.includes(color)
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-white text-gray-700 border-gray-300 hover:border-blue-400"
                    }`}
                  >
                    {color}
                  </button>
                ))}
              </div>
            </div>

            {/* Styles */}
            <div className="space-y-2">
              <Label>风格（可多选）</Label>
              <div className="flex flex-wrap gap-2">
                {STYLES.map((style) => (
                  <button
                    key={style}
                    type="button"
                    onClick={() =>
                      setFormData({
                        ...formData,
                        style: toggleSelection(formData.style, style),
                      })
                    }
                    className={`px-3 py-1 rounded-full text-sm border-2 transition ${
                      formData.style.includes(style)
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-white text-gray-700 border-gray-300 hover:border-blue-400"
                    }`}
                  >
                    {style}
                  </button>
                ))}
              </div>
            </div>

            {/* Seasons */}
            <div className="space-y-2">
              <Label>季节（可多选）</Label>
              <div className="flex flex-wrap gap-2">
                {SEASONS.map((season) => (
                  <button
                    key={season}
                    type="button"
                    onClick={() =>
                      setFormData({
                        ...formData,
                        season: toggleSelection(formData.season, season),
                      })
                    }
                    className={`px-3 py-1 rounded-full text-sm border-2 transition ${
                      formData.season.includes(season)
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-white text-gray-700 border-gray-300 hover:border-blue-400"
                    }`}
                  >
                    {season}
                  </button>
                ))}
              </div>
            </div>

            {/* Optional Fields */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="brand">品牌（可选）</Label>
                <Input
                  id="brand"
                  value={formData.brand}
                  onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                  placeholder="品牌名称"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="size">尺码（可选）</Label>
                <Input
                  id="size"
                  value={formData.size}
                  onChange={(e) => setFormData({ ...formData, size: e.target.value })}
                  placeholder="如：M, 38"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="material">材质（可选）</Label>
              <Input
                id="material"
                value={formData.material}
                onChange={(e) => setFormData({ ...formData, material: e.target.value })}
                placeholder="如：棉、麻、丝绸"
              />
            </div>

            <Button type="submit" className="w-full" disabled={saving || uploading}>
              {saving ? "保存中..." : uploading ? "上传中..." : "保存衣物"}
            </Button>
          </CardContent>
        </form>
      </Card>
    </div>
  )
}
