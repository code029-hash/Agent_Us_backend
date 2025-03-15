from transformers import pipeline

# Load paraphrasing model (T5-small)
paraphrase_pipeline = pipeline("text2text-generation", model="t5-small")

def change_tone(text, tone="neutral"):
    prompt = f"Rewrite this news in a {tone} tone:\n\n{text}"
    output = paraphrase_pipeline(prompt, max_length=100, truncation=True)
    return output[0]["generated_text"]
