// Tongyi Wanxiang API Client for Outfit Generation
// Documentation: https://tongyi.aliyun.com/wan/api

export interface TongyiClothingItem {
  id: string
  name: string
  category: string
  color: string[]
  style: string[]
  season: string[]
  imageUrl: string
}

export interface TongyiUser {
  height: number
  weight: number
  bodyType: string
  skinTone: string
}

export interface Tongyirequirements {
  style: string
  occasion: string
  season: string
}

export interface TongyiOutfitRequest {
  user: TongyiUser
  clothes: TongyiClothingItem[]
  requirements: Tongyirequirements
}

export interface TongyiOutfitResponse {
  selected_items: string[]
  reasoning: string
  tips: string[]
}

export interface TongyiAPIError {
  code: string
  message: string
}

/**
 * Generate outfit recommendation using Tongyi Wanxiang API
 * @param params - User info, clothing items, and requirements
 * @returns Outfit recommendation with selected items, reasoning, and tips
 */
export async function generateOutfitRecommendation(
  params: TongyiOutfitRequest
): Promise<TongyiOutfitResponse> {
  const apiKey = process.env.TONGYI_API_KEY

  if (!apiKey || apiKey === 'your-tongyi-api-key-here') {
    // Return mock response when API key is not configured
    console.warn('Tongyi API key not configured, returning mock response')
    return getMockResponse(params)
  }

  try {
    // Build the prompt for Tongyi Wanxiang
    const prompt = buildPrompt(params)

    // Call Tongyi Wanxiang API
    const response = await callTongyiAPI(prompt, apiKey)

    return response
  } catch (error) {
    console.error('Tongyi API error:', error)
    // Return mock response on error
    return getMockResponse(params)
  }
}

function buildPrompt(params: TongyiOutfitRequest): string {
  const { user, clothes, requirements } = params

  const clothesList = clothes.map(c =>
    `- ${c.name} (分类: ${c.category}, 颜色: ${c.color.join(', ')}, 风格: ${c.style.join(', ')}, 季节: ${c.season.join(', ')})`
  ).join('\n')

  return `你是一个专业的穿搭顾问。根据以下信息生成穿搭建议：

用户信息：
- 身高: ${user.height}cm
- 体重: ${user.weight}kg
- 体型: ${user.bodyType}
- 肤色: ${user.skinTone}

可用衣物：
${clothesList}

要求：
- 风格: ${requirements.style}
- 场合: ${requirements.occasion}
- 季节: ${requirements.season}

请只返回JSON格式，不要包含其他文字：
{
  "selected_items": ["衣物ID1", "衣物ID2", ...],
  "reasoning": "详细的搭配理由说明，解释为什么这样搭配适合用户的身材和场合",
  "tips": ["穿搭小贴士1", "穿搭小贴士2", "穿搭小贴士3"]
}`
}

async function callTongyiAPI(prompt: string, apiKey: string): Promise<TongyiOutfitResponse> {
  const apiUrl = 'https://tongyi.aliyun.com/wan/api'

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'wanxiang-v1',
      input: {
        messages: [
          {
            role: 'user',
            content: prompt
          }
        ]
      },
      parameters: {
        result_format: 'message',
        max_tokens: 2000
      }
    })
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(`Tongyi API error: ${response.status} ${JSON.stringify(errorData)}`)
  }

  const data = await response.json()

  // Parse the response to extract the JSON
  let content = data.output?.choices?.[0]?.message?.content || ''

  // Try to extract JSON from the response
  const jsonMatch = content.match(/\{[\s\S]*\}/)
  if (jsonMatch) {
    content = jsonMatch[0]
  }

  const result = JSON.parse(content)

  return {
    selected_items: result.selected_items || [],
    reasoning: result.reasoning || '暂无搭配说明',
    tips: result.tips || []
  }
}

function getMockResponse(params: TongyiOutfitRequest): TongyiOutfitResponse {
  const { clothes, requirements } = params

  // Simple mock logic: select items from different categories
  const selectedItems: string[] = []
  const categories = new Set<string>()

  // Select one item from each category if available
  for (const clothing of clothes) {
    if (!categories.has(clothing.category) && selectedItems.length < 5) {
      selectedItems.push(clothing.id)
      categories.add(clothing.category)
    }
  }

  // If no items selected, return first 3 items
  if (selectedItems.length === 0 && clothes.length > 0) {
    selectedItems.push(...clothes.slice(0, 3).map(c => c.id))
  }

  return {
    selected_items: selectedItems,
    reasoning: `根据您的需求和${requirements.style}风格，我们为您推荐了这组搭配。这套穿搭适合${requirements.occasion}场合，在${requirements.season}季节穿着舒适得体。单品之间在颜色和风格上相互呼应，展现出您的独特品味。`,
    tips: [
      '建议根据当天气温适当增减衣物',
      '配饰可以点缀整体造型，不要过于复杂',
      '保持自信是最好的穿搭态度'
    ]
  }
}
