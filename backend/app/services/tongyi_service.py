"""Tongyi Wanxiang API service for outfit generation."""
import os
import json
import re
import requests
from typing import List, Dict, Optional


def parse_json_array(json_string: str) -> List:
    """Parse JSON array string to list."""
    if not json_string:
        return []
    try:
        result = json.loads(json_string)
        return result if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


# Request/Response models for Tongyi API
class TongyiClothingItem:
    """Clothing item for Tongyi API request."""
    def __init__(self, id: str, name: str, category: str, color: List[str],
                 style: List[str], season: List[str], imageUrl: str):
        self.id = id
        self.name = name
        self.category = category
        self.color = color
        self.style = style
        self.season = season
        self.imageUrl = imageUrl


class TongyiUser:
    """User information for Tongyi API request."""
    def __init__(self, height: int, weight: int, body_type: str, skin_tone: str):
        self.height = height
        self.weight = weight
        self.body_type = body_type
        self.skin_tone = skin_tone


class TongyiRequirements:
    """Outfit requirements for Tongyi API request."""
    def __init__(self, style: str, occasion: str, season: str):
        self.style = style
        self.occasion = occasion
        self.season = season


class TongyiOutfitResponse:
    """Tongyi API response for outfit recommendation."""
    def __init__(self, selected_items: List[str], reasoning: str, tips: List[str]):
        self.selected_items = selected_items
        self.reasoning = reasoning
        self.tips = tips


def build_prompt(user: TongyiUser, clothes: List[TongyiClothingItem],
                  requirements: TongyiRequirements) -> str:
    """
    Build the prompt for Tongyi Wanxiang API.

    Args:
        user: User information
        clothes: List of clothing items
        requirements: Outfit requirements

    Returns:
        str: Formatted prompt for the AI
    """
    clothes_list = "\n".join([
        f"- {c.name} (分类: {c.category}, 颜色: {', '.join(c.color)}, "
        f"风格: {', '.join(c.style)}, 季节: {', '.join(c.season)})"
        for c in clothes
    ])

    return f"""你是一个专业的穿搭顾问。根据以下信息生成穿搭建议：

用户信息：
- 身高: {user.height}cm
- 体重: {user.weight}kg
- 体型: {user.body_type}
- 肤色: {user.skin_tone}

可用衣物：
{clothes_list}

要求：
- 风格: {requirements.style}
- 场合: {requirements.occasion}
- 季节: {requirements.season}

请只返回JSON格式，不要包含其他文字：
{{
  "selected_items": ["衣物ID1", "衣物ID2", ...],
  "reasoning": "详细的搭配理由说明，解释为什么这样搭配适合用户的身材和场合",
  "tips": ["穿搭小贴士1", "穿搭小贴士2", "穿搭小贴士3"]
}}"""


def call_tongyi_api(prompt: str, api_key: str) -> TongyiOutfitResponse:
    """
    Call the Tongyi Wanxiang API.

    Args:
        prompt: The prompt to send to the API
        api_key: Tongyi API key

    Returns:
        TongyiOutfitResponse: AI-generated outfit recommendation

    Raises:
        Exception: If API call fails
    """
    api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message",
            "max_tokens": 2000
        }
    }

    response = requests.post(api_url, headers=headers, json=payload, timeout=30)

    if response.status_code != 200:
        raise Exception(f"Tongyi API error: {response.status_code} {response.text}")

    data = response.json()

    # Parse response
    content = data.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")

    # Extract JSON from response
    json_match = re.search(r'\{[\s\S]*\}', content)
    if json_match:
        content = json_match.group(0)

    result = json.loads(content)

    return TongyiOutfitResponse(
        selected_items=result.get("selected_items", []),
        reasoning=result.get("reasoning", "暂无搭配说明"),
        tips=result.get("tips", [])
    )


def get_mock_response(clothes: List[TongyiClothingItem],
                      requirements: TongyiRequirements) -> TongyiOutfitResponse:
    """
    Generate a mock response when API is not configured.

    Args:
        clothes: List of clothing items
        requirements: Outfit requirements

    Returns:
        TongyiOutfitResponse: Mock outfit recommendation
    """
    selected_items: List[str] = []
    categories = set()

    # Select one item from each category
    for clothing in clothes:
        if clothing.category not in categories and len(selected_items) < 5:
            selected_items.append(clothing.id)
            categories.add(clothing.category)

    # If no items selected, return first 3 items
    if len(selected_items) == 0 and len(clothes) > 0:
        selected_items = [c.id for c in clothes[:3]]

    return TongyiOutfitResponse(
        selected_items=selected_items,
        reasoning=f"根据您的需求和{requirements.style}风格，我们为您推荐了这组搭配。"
                  f"这套穿搭适合{requirements.occasion}场合，在{requirements.season}季节穿着舒适得体。"
                  f"单品之间在颜色和风格上相互呼应，展现出您的独特品味。",
        tips=[
            "建议根据当天气温适当增减衣物",
            "配饰可以点缀整体造型，不要过于复杂",
            "保持自信是最好的穿搭态度"
        ]
    )


def generate_outfit_recommendation(
    user: Dict,
    clothes: List[Dict],
    requirements: Dict
) -> Dict:
    """
    Generate outfit recommendation using Tongyi Wanxiang API.

    Args:
        user: User information dict with keys: height, weight, bodyType, skinTone
        clothes: List of clothing item dicts
        requirements: Requirements dict with keys: style, occasion, season

    Returns:
        dict: AI-generated outfit recommendation with keys:
            selected_items, reasoning, tips
    """
    api_key = os.getenv('TONGYI_API_KEY', '')

    # Convert dicts to model objects
    user_obj = TongyiUser(
        height=user.get('height', 170),
        weight=user.get('weight', 65),
        body_type=user.get('bodyType', '标准'),
        skin_tone=user.get('skinTone', '中性')
    )

    clothes_objs = [
        TongyiClothingItem(
            id=c.get('id'),
            name=c.get('name'),
            category=c.get('category'),
            color=parse_json_array(c.get('color', '[]')),
            style=parse_json_array(c.get('style', '[]')),
            season=parse_json_array(c.get('season', '[]')),
            imageUrl=c.get('imageUrl')
        )
        for c in clothes
    ]

    requirements_obj = TongyiRequirements(
        style=requirements.get('style', '休闲'),
        occasion=requirements.get('occasion', '日常'),
        season=requirements.get('season', '春')
    )

    # Check if API key is configured
    if not api_key or api_key in ["your-tongyi-api-key-here", "your-tongyi-api-key-here"]:
        print("Tongyi API key not configured, returning mock response")
        mock_response = get_mock_response(clothes_objs, requirements_obj)
        return {
            "selected_items": mock_response.selected_items,
            "reasoning": mock_response.reasoning,
            "tips": mock_response.tips
        }

    # Build prompt
    prompt = build_prompt(user_obj, clothes_objs, requirements_obj)

    try:
        response = call_tongyi_api(prompt, api_key)
        return {
            "selected_items": response.selected_items,
            "reasoning": response.reasoning,
            "tips": response.tips
        }
    except Exception as e:
        print(f"Tongyi API error: {e}, returning mock response")
        mock_response = get_mock_response(clothes_objs, requirements_obj)
        return {
            "selected_items": mock_response.selected_items,
            "reasoning": mock_response.reasoning,
            "tips": mock_response.tips
        }
