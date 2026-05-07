import openai
import os
from models.generation import GenerationRequest, GenerationResult

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_image(req: GenerationRequest) -> GenerationResult:
    if req.model == 'dall-e-3':
        response = client.images.generate(
            model='dall-e-3',
            prompt=req.prompt,
            size=req.size,
            quality=req.quality,
            style=req.style,
            n=1
        )
        return GenerationResult(
            images=[{'url': img.url, 'revised_prompt': img.revised_prompt} for img in response.data],
            model=req.model,
            prompt=req.prompt
        )
    elif req.model == 'stable-diffusion':
        return generate_stable_diffusion(req)
    raise ValueError(f'Unsupported model: {req.model}')

def generate_stable_diffusion(req: GenerationRequest) -> GenerationResult:
    import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
    from stability_sdk import client as stability_client
    
    stability_api = stability_client.StabilityInference(
        key=os.getenv('STABILITY_API_KEY'),
        verbose=True,
        engine='stable-diffusion-xl-1024-v1-0'
    )
    
    answers = stability_api.generate(
        prompt=req.prompt,
        negative_prompt=req.negative_prompt,
        steps=30,
        cfg_scale=7.0,
        width=int(req.size.split('x')[0]),
        height=int(req.size.split('x')[1]),
        samples=req.n
    )
    
    images = []
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                images.append({'data': artifact.binary, 'seed': artifact.seed})
    
    return GenerationResult(images=images, model=req.model, prompt=req.prompt)
