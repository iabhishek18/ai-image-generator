from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from services.image_generator import generate_image
from services.upscaler import upscale_image
from models.generation import GenerationRequest
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    req = GenerationRequest(
        prompt=data['prompt'],
        negative_prompt=data.get('negative_prompt', ''),
        model=data.get('model', 'dall-e-3'),
        size=data.get('size', '1024x1024'),
        quality=data.get('quality', 'standard'),
        style=data.get('style', 'vivid'),
        n=data.get('n', 1)
    )
    result = generate_image(req)
    return jsonify({'success': True, 'data': result})

@app.route('/api/upscale', methods=['POST'])
def upscale():
    data = request.json
    result = upscale_image(data['image_url'], data.get('scale', 2))
    return jsonify({'success': True, 'data': result})

@app.route('/api/gallery', methods=['GET'])
def gallery():
    page = request.args.get('page', 1, type=int)
    return jsonify({'success': True, 'data': [], 'page': page})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
