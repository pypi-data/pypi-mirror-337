# Essential stopwords for product titles
STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this',
    'to', 'with', 'you', 'your'
}

def extract_title_tags(products, max_words=15, min_word_length=3):
    """
    Extract keywords from product titles, focusing on meaningful product terms.
    Automatically preserves multi-word product names (like 'washing machine').
    """
    word_counts = {}
    phrase_counts = {}
    
    if isinstance(products, str):
        products = [products]
    
    for item in products:
        title = getattr(item, 'product_title', item)
        if not isinstance(title, str):
            continue
            
        # Convert to lowercase and extract words
        words = []
        current_word = []
        for char in title.lower() + ' ':  # Add space to flush last word
            if char.isalpha():
                current_word.append(char)
            elif current_word:
                word = ''.join(current_word)
                if len(word) >= min_word_length and word not in STOPWORDS:
                    words.append(word)
                current_word = []
        
        # Count individual words and 2-word phrases
        for i, word in enumerate(words):
            word_counts[word] = word_counts.get(word, 0) + 1
            if i < len(words) - 1:
                phrase = f"{word} {words[i+1]}"
                phrase_counts[phrase] = phrase_counts.get(phrase, 0) + 1
    
    # Combine results prioritizing phrases
    combined = {**word_counts, **phrase_counts}
    return sorted(combined.keys(), key=lambda x: (-combined[x], x))[:max_words]