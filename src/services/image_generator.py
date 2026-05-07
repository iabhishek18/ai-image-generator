import openai
import os
from typing import List
from src.models.generation import GenerationRequest, GeneratedImage, GenerationResponse


def _get_client() -> openai.OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required. Set it in .env or environment.")
    return openai.OpenAI(api_key=key)


def generate_image(request: GenerationRequest) -> GenerationResponse:
    try:
        client = _get_client()

        if request.model == "dall-e-3":
            response = client.images.generate(
                model="dall-e-3",
                prompt=request.prompt,
                size=request.size,
                quality=request.quality,
                style=request.style,
                n=1,
            )

            images: List[GeneratedImage] = []
            for img_data in response.data:
                images.append(
                    GeneratedImage(
                        url=img_data.url or "",
                        revised_prompt=img_data.revised_prompt,
                        model="dall-e-3",
                        size=request.size,
                    )
                )

            return GenerationResponse(
                success=True,
                images=images,
                prompt=request.prompt,
                model="dall-e-3",
            )

        elif request.model == "dall-e-2":
            response = client.images.generate(
                model="dall-e-2",
                prompt=request.prompt,
                size=request.size,
                n=min(request.n, 4),
            )

            images = [
                GeneratedImage(url=img.url or "", model="dall-e-2", size=request.size)
                for img in response.data
            ]

            return GenerationResponse(
                success=True,
                images=images,
                prompt=request.prompt,
                model="dall-e-2",
            )

        else:
            return GenerationResponse(
                success=False,
                error=f"Unsupported model: {request.model}. Supported: dall-e-3, dall-e-2",
            )

    except openai.BadRequestError as e:
        return GenerationResponse(
            success=False,
            error=f"OpenAI rejected the request: {str(e)}",
            prompt=request.prompt,
        )
    except openai.AuthenticationError:
        return GenerationResponse(
            success=False, error="Invalid API key. Check your OPENAI_API_KEY."
        )
    except openai.RateLimitError:
        return GenerationResponse(
            success=False, error="Rate limit exceeded. Please wait and try again."
        )
    except Exception as e:
        return GenerationResponse(success=False, error=f"Generation failed: {str(e)}")


def create_variation(
    image_url: str, n: int = 1, size: str = "1024x1024"
) -> GenerationResponse:
    try:
        client = _get_client()
        import requests as req
        import io

        img_response = req.get(image_url, timeout=30)
        img_bytes = io.BytesIO(img_response.content)
        img_bytes.name = "image.png"

        response = client.images.create_variation(
            image=img_bytes,
            n=n,
            size=size,
        )

        images = [
            GeneratedImage(url=img.url or "", model="dall-e-2", size=size)
            for img in response.data
        ]
        return GenerationResponse(success=True, images=images, model="dall-e-2")

    except Exception as e:
        return GenerationResponse(success=False, error=f"Variation failed: {str(e)}")
