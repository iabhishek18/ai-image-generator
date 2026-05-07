from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class GenerationRequest:
    prompt: str
    negative_prompt: str = ''
    model: str = 'dall-e-3'
    size: str = '1024x1024'
    quality: str = 'standard'
    style: str = 'vivid'
    n: int = 1

@dataclass
class GenerationResult:
    images: List[Dict[str, Any]] = field(default_factory=list)
    model: str = ''
    prompt: str = ''
