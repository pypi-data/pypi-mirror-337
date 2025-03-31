import base64
from enum import Enum

import httpx
from mcp.types import TextContent, ImageContent

SIEU_NHAN_API_BASE = 'https://script.google.com/macros/s/AKfycbyGg3Wk3hWnLTGw_PLkNTFqAhpdln-pg9tkJlBGLn8MafiElQsi89QwtEQP2GfFMBxQ/exec'


class SieuNhanTools(str, Enum):
    GET_SIEU_NHAN = 'get_sieu_nhan'


async def get_sieu_nhan():
    """
    Get a random superhero from the API.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(SIEU_NHAN_API_BASE)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data
        except httpx.RequestError as e:
            print(f"An error occurred while requesting the API: {e}")
            return None


async def get_image_base64(img_url: str) -> str | None:
    """
    Fetch an image from the given URL and return its base64-encoded data.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(img_url)
            response.raise_for_status()
            image_data = response.content
            base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded_data
        except httpx.RequestError as e:
            print(f"An error occurred while requesting the image: {e}")
            return None


async def get_sieu_nhan_tools() -> TextContent | ImageContent:
    """
    Get a random superhero from the API and format it for display.
    """
    data = await get_sieu_nhan()
    if data:
        image_url = data.get('image')
        if image_url:
            base64_image = await get_image_base64(image_url)
            if base64_image:
                return ImageContent(
                    type="image",
                    data=base64_image,
                    mimeType="image/jpeg",
                )
            else:
                return TextContent(type="text", text="Failed to retrieve image.")
        else:
            return TextContent(type="text", text="No image URL found in the response.")
    else:
        return TextContent(type="text", text="Failed to retrieve superhero data.")
