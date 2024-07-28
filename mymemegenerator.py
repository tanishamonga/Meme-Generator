# mymemegenerator.py

import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image, ImageDraw, ImageFont
import os

class MemeGenerator:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.model_name = "gpt2"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.font_path = "arial.ttf"  # Path to a .ttf font file

    def generate_caption(self, prompt):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=50, num_return_sequences=1)
        caption = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return caption

    def select_random_image(self):
        images = [os.path.join(self.image_folder, img) for img in os.listdir(self.image_folder) if img.endswith(('jpg', 'jpeg', 'png'))]
        return random.choice(images)

    def load_image(self, image_path):
        return Image.open(image_path)

    def add_caption_to_image(self, image, caption, position="bottom", font_size=30, text_color="white"):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, font_size)
        text_width, text_height = draw.textsize(caption, font=font)
        width, height = image.size

        if position == "bottom":
            x = (width - text_width) / 2
            y = height - text_height - 10
        elif position == "top":
            x = (width - text_width) / 2
            y = 10
        else:
            x = (width - text_width) / 2
            y = (height - text_height) / 2

        draw.text((x, y), caption, font=font, fill=text_color)
        return image
