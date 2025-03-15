from transformers import pipeline

paraphrase_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def change_tone(text, tone="neutral"):
    prompt = f"Rewrite this in a {tone} tone: {text}"
    output = paraphrase_pipeline(prompt, max_length=100, truncation=True)
    return output[0]["summary_text"]
