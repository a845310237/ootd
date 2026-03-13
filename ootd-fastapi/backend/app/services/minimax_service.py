"""MiniMax Image-01 AI service for outfit image generation."""
import httpx
import json
from typing import Optional, List
from app.core.config import settings


class MiniMaxService:
    """MiniMax AI service for image generation."""

    def __init__(self):
        """Initialize MiniMax service."""
        self.api_key = settings.MINIMAX_API_KEY
        self.group_id = settings.MINIMAX_GROUP_ID
        self.base_url = "https://api.minimaxi.com/v1/image_generation"

    async def generate_outfit_image(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        n: int = 1,
        prompt_optimizer: bool = True,
        reference_image: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate outfit image using MiniMax Image-01 model.

        Args:
            prompt: Text description of the outfit to generate
            aspect_ratio: Image aspect ratio (16:9, 4:3, 1:1, 3:4, 9:16)
            n: Number of images to generate
            prompt_optimizer: Whether to use prompt optimizer
            reference_image: Optional URL of reference image to guide generation

        Returns:
            Image URL or None if generation fails
        """
        if not self.api_key or not self.group_id:
            print("MiniMax API key or group ID not configured")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Enhance prompt with reference image if provided
        enhanced_prompt = prompt
        if reference_image:
            enhanced_prompt = f"{prompt}\n\nReference image for style and body type: {reference_image}\nPlease generate a similar outfit composition while maintaining the person's body characteristics and pose style."

        payload = {
            "model": "image-01",
            "prompt": enhanced_prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": n,
            "prompt_optimizer": prompt_optimizer
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    # Return the first image URL
                    if data.get("data") and len(data["data"]) > 0:
                        return data["data"][0].get("url")
                    else:
                        print(f"MiniMax API error: No image data in response")
                        return None
                else:
                    print(f"MiniMax API error: {response.status_code} - {response.text}")
                    return None

        except Exception as e:
            print(f"MiniMax API exception: {str(e)}")
            return None

    def build_outfit_prompt(
        self,
        user_description: str,
        clothing_items: List[str],
        style: str,
        occasion: str,
        season: str
    ) -> str:
        """
        Build a prompt for outfit image generation.

        Args:
            user_description: Description of the user (height, body type, etc.)
            clothing_items: List of clothing item descriptions
            style: Style preference
            occasion: Occasion for the outfit
            season: Season for the outfit

        Returns:
            Formatted prompt for image generation
        """
        clothing_desc = ", ".join(clothing_items)

        prompt = f"""A professional fashion photo showing a person wearing: {clothing_desc}.

The person has {user_description}.

The outfit style is {style}, suitable for {occasion} occasion during {season} season.

Requirements:
- Full body shot, standing pose
- Clean, well-lit background (white or light gray studio background)
- Professional fashion photography style
- High quality, detailed, photorealistic
- Show the outfit clearly with good lighting

Please generate a realistic fashion photo showing how these clothing items would look when worn together."""

        return prompt


# Singleton instance
minimax_service = MiniMaxService()
