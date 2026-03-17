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
        if not self.api_key:
            print("MiniMax API key not configured")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Build base payload
        payload = {
            "model": "image-01",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": n,
            "prompt_optimizer": prompt_optimizer
        }

        # Add reference image if provided
        if reference_image:
            # Download and encode reference image to base64
            try:
                import httpx
                print(f"Attempting to download reference image from: {reference_image}")
                async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as img_client:
                    img_response = await img_client.get(reference_image)
                    if img_response.status_code == 200:
                        import base64
                        image_base64 = base64.b64encode(img_response.content).decode('utf-8')
                        # Try to add reference image to payload
                        # Note: Check if MiniMax Image-01 supports this parameter
                        payload["image_base64"] = [
                            {
                                "image": image_base64,
                                "prompt": "reference image for person and style"
                            }
                        ]
                        print(f"✓ Successfully added reference image to payload (base64 length: {len(image_base64)})")
                    else:
                        print(f"✗ Failed to download reference image: HTTP {img_response.status_code}")
            except Exception as e:
                print(f"✗ Error processing reference image: {str(e)}")
                print("  Continuing with text-only prompt generation...")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    print(f"MiniMax API response data: {data}")
                    # Handle different response formats
                    if data.get("data"):
                        # Format: {"data": {"image_urls": [...]}}
                        if "image_urls" in data["data"]:
                            if len(data["data"]["image_urls"]) > 0:
                                print(f"MiniMax API success: Got image URL from image_urls")
                                return data["data"]["image_urls"][0]
                        # Format: {"data": [{"url": ...}]}
                        elif len(data["data"]) > 0:
                            print(f"MiniMax API success: Got image URL from data array")
                            return data["data"][0].get("url")
                    print(f"MiniMax API error: No image data in response, data keys: {list(data.keys())}")
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
        season: str,
        custom_description: str = None
    ) -> str:
        """
        Build a prompt for outfit image generation.

        Args:
            user_description: Description of the user (height, body type, etc.)
            clothing_items: List of clothing item descriptions
            style: Style preference
            occasion: Occasion for the outfit
            season: Season for the outfit
            custom_description: Custom description for the outfit (optional)

        Returns:
            Formatted prompt for image generation
        """
        clothing_desc = ", ".join(clothing_items)

        # Build base prompt
        prompt = f"""A professional fashion photo showing a person wearing: {clothing_desc}.

The person has {user_description}.

The outfit style is {style}, suitable for {occasion} occasion during {season} season."""

        # Add custom description if provided
        if custom_description:
            prompt += f"""

Additional requirements: {custom_description}"""

        # Add standard requirements
        prompt += """

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
