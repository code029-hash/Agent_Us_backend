from PIL import Image, ImageDraw, ImageFont

def create_meme(text, image_path="trump.jpg", output_path="meme.jpg"):
    """Generates a meme with overlaid text."""
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Load a font
        font = ImageFont.truetype("arial.ttf", 40)

        # Calculate text position (centered)
        img_width, img_height = img.size
        text_width, text_height = draw.textsize(text, font=font)
        position = ((img_width - text_width) // 2, img_height - text_height - 50)

        # Add text to image
        draw.text(position, text, fill="white", font=font, stroke_width=2, stroke_fill="black")

        img.save(output_path)
        return output_path
    except Exception as e:
        return str(e)
