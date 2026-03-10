"use client"

import { useState, useEffect } from "react"
import { useSession } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function ProfilePage() {
  const { data: session, update } = useSession()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    height: "",
    weight: "",
    bodyType: "标准",
    skinTone: "中性",
  })
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Fetch current profile
    const fetchProfile = async () => {
      const response = await fetch("/api/user/profile")
      const data = await response.json()
      setFormData({
        name: data.name || "",
        email: data.email || "",
        height: data.height?.toString() || "",
        weight: data.weight?.toString() || "",
        bodyType: data.bodyType || "标准",
        skinTone: data.skinTone || "中性",
      })
    }
    fetchProfile()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage("")
    setLoading(true)

    try {
      const response = await fetch("/api/user/profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.name,
          height: formData.height ? parseInt(formData.height) : null,
          weight: formData.weight ? parseInt(formData.weight) : null,
          bodyType: formData.bodyType,
          skinTone: formData.skinTone,
        }),
      })

      if (response.ok) {
        setMessage("个人资料已更新")
        // Update session
        await update({ name: formData.name })
      } else {
        setMessage("更新失败，请稍后重试")
      }
    } catch (err) {
      setMessage("更新失败，请稍后重试")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>个人资料</CardTitle>
          <CardDescription>
            更新您的个人信息，帮助我们为您提供更好的穿搭建议
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {message && (
              <div className="bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md text-sm">
                {message}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">邮箱</Label>
              <Input id="email" value={formData.email} disabled />
              <p className="text-xs text-gray-500">邮箱无法修改</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="name">姓名</Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="height">身高 (cm)</Label>
                <Input
                  id="height"
                  name="height"
                  type="number"
                  value={formData.height}
                  onChange={handleChange}
                  placeholder="170"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="weight">体重 (kg)</Label>
                <Input
                  id="weight"
                  name="weight"
                  type="number"
                  value={formData.weight}
                  onChange={handleChange}
                  placeholder="65"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bodyType">体型</Label>
                <select
                  id="bodyType"
                  name="bodyType"
                  value={formData.bodyType}
                  onChange={handleChange}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                >
                  <option value="苗条">苗条</option>
                  <option value="标准">标准</option>
                  <option value="丰满">丰满</option>
                </select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="skinTone">肤色</Label>
                <select
                  id="skinTone"
                  name="skinTone"
                  value={formData.skinTone}
                  onChange={handleChange}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                >
                  <option value="偏白">偏白</option>
                  <option value="中性">中性</option>
                  <option value="偏黑">偏黑</option>
                </select>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "保存中..." : "保存更改"}
            </Button>
          </CardContent>
        </form>
      </Card>
    </div>
  )
}
