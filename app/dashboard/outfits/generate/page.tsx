"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import Image from "next/image"
import { Sparkles, Loader2 } from "lucide-react"

const STYLES = ["休闲", "正式", "运动", "复古", "简约", "时尚", "街头", "商务", "甜美", "酷帅"]
const OCCASIONS = ["日常", "工作", "约会", "聚会", "运动", "旅行", "正式场合", "休闲场合"]
const SEASONS = ["春", "夏", "秋", "冬"]

export default function GenerateOutfitPage() {
  const router = useRouter()
  const [requirements, setRequirements] = useState({
    style: "休闲",
    occasion: "日常",
    season: "春",
  })
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [saving, setSaving] = useState(false)
  const [outfitName, setOutfitName] = useState("")

  const handleGenerate = async () => {
    setGenerating(true)
    setResult(null)

    try {
      const response = await fetch("/api/outfits/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requirements),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "生成失败")
      }

      setResult(data)
      setOutfitName(`${requirements.style}风${requirements.occasion}穿搭`)
    } catch (error) {
      alert(error instanceof Error ? error.message : "生成失败")
    } finally {
      setGenerating(false)
    }
  }

  const handleSave = async () => {
    if (!result) return

    setSaving(true)

    try {
      const response = await fetch("/api/outfits/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: outfitName,
          style: requirements.style,
          occasion: requirements.occasion,
          season: requirements.season,
          selectedItems: result.selected_items.map((item: any) => item.id),
          reasoning: result.reasoning,
          tips: result.tips,
          aiGenerated: true,
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

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI智能搭配</h1>
        <p className="text-gray-600 mt-1">
          告诉我们您的需求，AI将为您的衣柜中的衣物生成搭配建议
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>选择您的需求</CardTitle>
          <CardDescription>
            AI将根据您的选择和衣柜中的衣物为您生成搭配
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Style Selection */}
          <div className="space-y-3">
            <label className="text-sm font-medium">风格</label>
            <div className="flex flex-wrap gap-2">
              {STYLES.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setRequirements({ ...requirements, style: s })}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    requirements.style === s
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Occasion Selection */}
          <div className="space-y-3">
            <label className="text-sm font-medium">场合</label>
            <div className="flex flex-wrap gap-2">
              {OCCASIONS.map((o) => (
                <button
                  key={o}
                  type="button"
                  onClick={() => setRequirements({ ...requirements, occasion: o })}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    requirements.occasion === o
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {o}
                </button>
              ))}
            </div>
          </div>

          {/* Season Selection */}
          <div className="space-y-3">
            <label className="text-sm font-medium">季节</label>
            <div className="flex flex-wrap gap-2">
              {SEASONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setRequirements({ ...requirements, season: s })}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    requirements.season === s
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <Button
            onClick={handleGenerate}
            disabled={generating}
            className="w-full"
            size="lg"
          >
            {generating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                AI正在为您搭配...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                开始AI搭配
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>AI搭配建议</CardTitle>
            <CardDescription>
              根据您的需求，AI为您生成了以下搭配方案
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Outfit Name */}
            <div>
              <label className="text-sm font-medium block mb-2">保存为穿搭方案</label>
              <input
                type="text"
                value={outfitName}
                onChange={(e) => setOutfitName(e.target.value)}
                className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                placeholder="输入方案名称"
              />
            </div>

            {/* Selected Items */}
            <div>
              <h3 className="font-medium mb-3">推荐单品</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {result.selected_items.map((item: any) => (
                  <div key={item.id} className="relative aspect-square bg-gray-100 rounded-lg overflow-hidden">
                    <Image
                      src={item.imageUrl || "/placeholder-clothing.jpg"}
                      alt={item.name}
                      fill
                      className="object-cover"
                      sizes="(max-width: 768px) 50vw, 25vw"
                    />
                    <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white p-2 text-sm">
                      {item.name}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Reasoning */}
            {result.reasoning && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h3 className="font-medium mb-2 text-blue-900">搭配理由</h3>
                <p className="text-blue-800 text-sm">{result.reasoning}</p>
              </div>
            )}

            {/* Tips */}
            {result.tips && result.tips.length > 0 && (
              <div>
                <h3 className="font-medium mb-2">穿搭小贴士</h3>
                <ul className="space-y-2">
                  {result.tips.map((tip: string, index: number) => (
                    <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="text-blue-600 mt-1">•</span>
                      {tip}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <Button onClick={handleSave} disabled={saving} className="w-full">
              {saving ? "保存中..." : "保存穿搭方案"}
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
