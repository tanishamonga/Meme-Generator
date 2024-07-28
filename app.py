# app.py

from flask import Flask, request, jsonify, send_from_directory
from mymemegenerator import MemeGenerator
from PIL import Image
import io
import base64
import os

app = Flask(__name__)
meme_generator = MemeGenerator('meme_images')

@app.route('/generate_caption', methods=['POST'])
def generate_caption():
    prompt = request.json['prompt']
    caption = meme_generator.generate_caption(prompt)
    return jsonify({'caption': caption})

@app.route('/generate_meme', methods=['POST'])
def generate_meme():
    data = request.json
    caption_type = data['captionType']
    caption = data['caption'] if caption_type == 'manual' else meme_generator.generate_caption(data['aiPrompt'])
    position = data.get('position', 'bottom')
    font_size = data.get('fontSize', 30)
    text_color = data.get('textColor', 'white')

    image_file = meme_generator.select_random_image()
    image = meme_generator.load_image(image_file)
    image_with_caption = meme_generator.add_caption_to_image(image, caption, position, font_size, text_color)

    img_byte_arr = io.BytesIO()
    image_with_caption.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

    return jsonify({'image': img_base64})

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
