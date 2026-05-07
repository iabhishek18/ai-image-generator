from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class GenerationRequest:
    prompt: str
    negative_prompt: str = ""
    model: str = "dall-e-3"
    size: str = "1024x1024"
    quality: str = "standard"
    style: str = "vivid"
    n: int = 1


@dataclass
class GeneratedImage:
    url: str
    revised_prompt: Optional[str] = None
    model: str = ""
    size: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class GenerationResponse:
    success: bool
    images: List[GeneratedImage] = field(default_factory=list)
    prompt: str = ""
    model: str = ""
    error: Optional[str] = None
