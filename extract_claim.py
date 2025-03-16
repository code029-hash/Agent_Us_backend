import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

nlp = spacy.load("en_core_web_sm")

def extract_main_claim(text):
    """
    Extracts the most important claim from a given news summary.
    Uses keyword extraction & sentence ranking.
    """
    if not text or len(text) < 20:
        return "No valid claim found"

    # Use NLP to find named entities (e.g., people, organizations)
    doc = nlp(text)
    entities = {ent.text for ent in doc.ents if ent.label_ in {"ORG", "PERSON", "GPE", "EVENT"}}

    # Summarize text using LSA (Latent Semantic Analysis)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, 1)

    if summary_sentences:
        claim = str(summary_sentences[0])
    else:
        claim = text[:150]  # Fallback to first 150 chars if summarization fails

    # Include important named entities in claim
    for entity in entities:
        if entity in text:
            claim = f"{entity}: {claim}"

    return claim.strip()
