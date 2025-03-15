from transformers import pipeline
import torch

def change_tone(text, tone="neutral"):
    # Load model only when needed and use CPU
    paraphrase_pipeline = pipeline(
        "summarization",
        model="facebook/bart-base-cnn",  # Smaller base model
        device="cpu",  # Force CPU usage
        torch_dtype=torch.float16 if torch.cuda.is_available() else None
    )

    prompt = f"Rewrite this in a {tone} tone: {text}"
    output = paraphrase_pipeline(
        prompt,
        max_length=100,
        truncation=True,
        no_repeat_ngram_size=2  # Reduce computation
    )
    return output[0]["summary_text"]