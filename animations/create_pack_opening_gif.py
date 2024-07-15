import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from io import BytesIO
import numpy as np
import os

# Step 1: Download the image
url = "https://www.upperdeckepack.com/Images/Packs/2023-24-UD-Series-2-Hockey_Medium.png"
response = requests.get(url)
pack_image = Image.open(BytesIO(response.content)).convert('RGBA')

# Step 2: Simulate pack opening with colorful sparkles and glows
frames = []
num_frames = 30

# Generate frames for pack opening
for i in range(num_frames):
    frame = pack_image.copy()
    draw = ImageDraw.Draw(frame)

    # Add colorful sparkles
    if i > num_frames // 2:
        num_sparkles = (i - num_frames // 2) * 10
        for _ in range(num_sparkles):
            # Random position and size
            x = np.random.randint(0, frame.width)
            y = np.random.randint(0, frame.height)
            size = np.random.randint(1, 6)
            # Random color
            color = tuple(np.random.randint(100, 256, size=3)) + (255,)
            draw.ellipse((x, y, x+size, y+size), fill=color)

        # Add glow effect
        if i % 2 == 0:  # Apply glow every other frame for a blinking effect
            frame = frame.filter(ImageFilter.GaussianBlur(radius=2))

    frames.append(frame)

# Enhance frames for better visual effect
enhanced_frames = []
for frame in frames:
    enhancer = ImageEnhance.Brightness(frame)
    enhanced_frame = enhancer.enhance(1.2)  # Slightly brighten the frame
    enhanced_frames.append(enhanced_frame)

# Ensure the 'animations' folder exists in the directory from which the script is run
script_dir = os.path.dirname(os.path.realpath(__file__))
animations_dir = os.path.join(script_dir, 'animations')
os.makedirs(animations_dir, exist_ok=True)

# Save the animation to the 'animations' folder
output_path = os.path.join(animations_dir, 'enhanced_pack_opening.gif')
enhanced_frames[0].save(output_path, save_all=True, append_images=enhanced_frames[1:], loop=0, duration=100)

print(f"Animation saved as {output_path}")
