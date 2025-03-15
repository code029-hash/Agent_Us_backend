def summarize_text(text):
    """Generate a coherent summary in 50-60 words."""
    try:
        cleaned = clean_text(text)
        words = cleaned.split()

        if len(words) < 50:
            return cleaned

        sentences = sent_tokenize(cleaned)
        if len(sentences) < 3:
            return ' '.join(words[:60])

        stop_words = set(stopwords.words('english'))
        keywords = [word.lower() for word in words if word.lower() not in stop_words and len(word) > 2]

        word_freq = nltk.FreqDist(keywords)
        max_freq = max(word_freq.values(), default=1)

        sentence_scores = {}
        for i, sent in enumerate(sentences):
            sent_words = [word.lower() for word in word_tokenize(sent)]
            score = sum(word_freq[word] / max_freq for word in sent_words if word in word_freq)
            sentence_scores[i] = score / len(sent_words)  # Normalize score

        sorted_sents = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary = []
        word_count = 0

        for idx, _ in sorted_sents:
            sent_words = sentences[idx].split()
            if word_count + len(sent_words) <= 60:
                summary.append(sentences[idx])
                word_count += len(sent_words)
                if word_count >= 50:
                    break

        if 50 <= word_count <= 60:
            return ' '.join(summary)

        fallback = []
        current_words = 0
        for sent in sentences:
            sent_words = sent.split()
            if current_words + len(sent_words) <= 60:
                fallback.append(sent)
                current_words += len(sent_words)
            else:
                remaining = 60 - current_words
                if remaining > 3:
                    fallback.append(' '.join(sent_words[:remaining]))
                break

        return ' '.join(fallback)

    except Exception as e:
        logging.error(f"Summarization error: {str(e)}")
        return ' '.join(cleaned.split()[:60])  
