#future advancement
from diffusers import StableDiffusionPipeline
import torch

# Load Stable Diffusion model (less restrictive)
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

# Disable NSFW filter (Optional, for advanced users)
pipe.safety_checker = lambda images, **kwargs: (images, False)

def generate_meme(text):
    prompt = f"A humorous cartoon meme about: {text}, no nudity, no violence, safe for work"
    image = pipe(prompt).images[0]
    image.save("meme.png")
    print("✅ Meme saved as meme.png")

# Example usage
generate_meme("When AI takes over the world")
