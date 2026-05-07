from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.services.image_generator import generate_image, create_variation
from src.models.generation import GenerationRequest

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/health")
def health():
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    return jsonify(
        {
            "status": "ok",
            "version": "2.0.0",
            "openai_configured": has_key,
            "supported_models": ["dall-e-3", "dall-e-2"],
            "supported_sizes": [
                "1024x1024",
                "1024x1792",
                "1792x1024",
                "512x512",
                "256x256",
            ],
        }
    )


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    if not data or not data.get("prompt"):
        return jsonify({"success": False, "error": "prompt is required"}), 400

    prompt = data["prompt"].strip()
    if len(prompt) < 3:
        return jsonify(
            {"success": False, "error": "prompt must be at least 3 characters"}
        ), 400
    if len(prompt) > 4000:
        return jsonify(
            {"success": False, "error": "prompt must be under 4000 characters"}
        ), 400

    req = GenerationRequest(
        prompt=prompt,
        negative_prompt=data.get("negative_prompt", ""),
        model=data.get("model", "dall-e-3"),
        size=data.get("size", "1024x1024"),
        quality=data.get("quality", "standard"),
        style=data.get("style", "vivid"),
        n=data.get("n", 1),
    )

    result = generate_image(req)

    if not result.success:
        return jsonify({"success": False, "error": result.error}), 422

    return jsonify(
        {
            "success": True,
            "data": {
                "images": [
                    {
                        "url": img.url,
                        "revised_prompt": img.revised_prompt,
                        "model": img.model,
                        "size": img.size,
                        "created_at": img.created_at,
                    }
                    for img in result.images
                ],
                "prompt": result.prompt,
                "model": result.model,
            },
        }
    )


@app.route("/api/variation", methods=["POST"])
def variation():
    data = request.json
    if not data or not data.get("image_url"):
        return jsonify({"success": False, "error": "image_url is required"}), 400

    result = create_variation(
        image_url=data["image_url"],
        n=data.get("n", 1),
        size=data.get("size", "1024x1024"),
    )

    if not result.success:
        return jsonify({"success": False, "error": result.error}), 422

    return jsonify(
        {
            "success": True,
            "data": {
                "images": [
                    {"url": img.url, "model": img.model} for img in result.images
                ]
            },
        }
    )


@app.route("/api/models", methods=["GET"])
def list_models():
    return jsonify(
        {
            "success": True,
            "data": [
                {
                    "id": "dall-e-3",
                    "name": "DALL-E 3",
                    "description": "Latest model with best quality and prompt understanding",
                    "max_size": "1792x1024",
                    "supports_style": True,
                    "supports_quality": True,
                },
                {
                    "id": "dall-e-2",
                    "name": "DALL-E 2",
                    "description": "Faster, supports multiple images and variations",
                    "max_size": "1024x1024",
                    "supports_style": False,
                    "supports_quality": False,
                },
            ],
        }
    )


@app.route("/api/prompt-templates", methods=["GET"])
def templates():
    return jsonify(
        {
            "success": True,
            "data": [
                {
                    "category": "Art",
                    "prompts": [
                        "A surrealist painting of a floating city above clouds, oil on canvas style",
                        "A watercolor illustration of a Japanese garden in autumn",
                        "An impressionist painting of a busy Paris café at night",
                    ],
                },
                {
                    "category": "Photography",
                    "prompts": [
                        "Professional headshot of a business executive, studio lighting, shallow depth of field",
                        "Aerial drone photo of a tropical island with crystal clear water",
                        "Street photography of Tokyo at night, neon lights, rain reflections",
                    ],
                },
                {
                    "category": "Design",
                    "prompts": [
                        "Minimalist logo design for a tech startup, clean lines, modern typography",
                        "Mobile app UI design for a fitness tracker, dark mode, gradient accents",
                        "Product packaging design for premium chocolate brand, elegant and luxurious",
                    ],
                },
                {
                    "category": "3D",
                    "prompts": [
                        "Isometric 3D render of a cozy home office setup, soft lighting",
                        "Low-poly 3D landscape with mountains and a river at sunset",
                        "Cyberpunk cityscape in 3D, volumetric lighting, futuristic architecture",
                    ],
                },
            ],
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5007))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"[AI Image Generator] Starting on port {port}")
    print(f"[OpenAI] API Key configured: {bool(os.getenv('OPENAI_API_KEY'))}")
    app.run(host="0.0.0.0", port=port, debug=debug)
