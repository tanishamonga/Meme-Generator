import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import textwrap

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Path to the folder containing meme images
meme_images_path = 'D:\Meme generation\meme_images'  # Update this with the correct path

def generate_caption(prompt, emotion=None):
    if emotion and emotion != "None":
        prompt = f"{emotion.capitalize()} caption: {prompt}"
    
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(
        input_ids,
        max_length=30,
        num_return_sequences=1,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    caption = tokenizer.decode(output[0], skip_special_tokens=True)
    caption = caption[len(prompt):].strip()
    max_length = 100
    if len(caption) > max_length:
        caption = caption[:max_length] + '...'
    return caption

def add_caption_to_image(image, caption, position, font, font_size, font_color):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font, font_size)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    width, height = image.size

    if position == "bottom":
        x = (width - text_width) / 2
        y = height - text_height - 10
    elif position == "top":
        x = (width - text_width) / 2
        y = 10
    elif position == "left":
        x = 10
        y = (height - text_height) / 2
    elif position == "right":
        x = width - text_width - 10
        y = (height - text_height) / 2
    else:
        x = (width - text_width) / 2
        y = (height - text_height) / 2

    draw.text((x, y), caption, font=font, fill=font_color)
    return image

def select_image_by_keyword(keyword):
    keyword_to_images = {
        "animal": ["animal.jpeg"],
        "city": ["city.jpg"],
        "fire": ["fire.jpg"],
        "river": ["river.jpg", "river2.jpg"],
        "car": ["car.jpg", "car (1).jpg"],
        "smile": ["smile.jpg"],
        # Add more keywords and images here
    }
    if keyword in keyword_to_images:
        images = keyword_to_images[keyword]
        return random.choice(images)
    else:
        return random.choice(os.listdir(meme_images_path))

# Streamlit app
st.title("Meme Generator")

# Sidebar for user inputs
st.sidebar.header("Customize Your Meme")
caption_type = st.sidebar.selectbox("Caption Type", ["Manual", "AI"])
caption_input = st.sidebar.text_input("Caption", value="Your meme caption here")
position_input = st.sidebar.selectbox("Caption Position", ["top", "bottom", "left", "right"], index=1)
font_input = st.sidebar.text_input("Font Path", value="arial.ttf")
font_size_input = st.sidebar.slider("Font Size", 10, 100, 20)
font_color_input = st.sidebar.color_picker("Font Color", "#FFFFFF")
emotion_input = st.sidebar.selectbox("Emotion", ["None", "Happy", "Sad", "Stressed", "Funny"], index=0)
ai_prompt_input = st.sidebar.text_input("AI Prompt", value="Generate a funny meme caption")
keyword_input = st.sidebar.text_input("Keyword", value="animal")

uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
else:
    image_path = select_image_by_keyword(keyword_input)
    image = Image.open(os.path.join(meme_images_path, image_path))

if caption_type == "AI":
    caption = generate_caption(ai_prompt_input, emotion=emotion_input)
else:
    caption = caption_input

if st.sidebar.button("Generate Meme"):
    meme = add_caption_to_image(image, caption, position_input, font_input, font_size_input, font_color_input)
    st.image(meme, caption="Generated Meme", use_column_width=True)
