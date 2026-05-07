# AI Image Generator — DALL-E & Stable Diffusion

> Multi-model text-to-image generation platform supporting DALL-E 3 and Stable Diffusion XL with upscaling, gallery, and batch generation.

## 🚀 Overview

A text-to-image generation platform that supports multiple AI models (OpenAI DALL-E 3 and Stability AI's Stable Diffusion XL). Features include prompt engineering templates, image upscaling, a community gallery, and batch generation — all served via a Flask REST API with S3 storage.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎨 DALL-E 3 | OpenAI's latest image model |
| 🖼️ Stable Diffusion XL | Open-source alternative |
| ⬆️ Image Upscaling | 2x/4x resolution enhancement |
| 📦 Batch Generation | Generate multiple images at once |
| 🖌️ Prompt Templates | Pre-built prompt starters |
| 🏛️ Gallery | Community sharing + browsing |
| ☁️ S3 Storage | Persistent image storage |
| 🔧 Style Control | Vivid/natural style selection |

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| API | Python, Flask |
| AI Models | OpenAI (DALL-E 3), Stability AI (SDXL) |
| Storage | AWS S3 |
| Queue | Celery + Redis |
| Frontend | React |

## ⚡ Quick Start

```bash
cd src && pip install -r ../requirements.txt
cp ../.env.example ../.env
python api/app.py
```

API at `http://localhost:5000` | Endpoints: POST `/api/generate`, POST `/api/upscale`, GET `/api/gallery`

## 📄 License

MIT
