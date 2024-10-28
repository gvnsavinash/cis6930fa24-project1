import os
import re

def apply_redaction(text, entities, redact_names=False, redact_dates=False, redact_phones=False, redact_address=False, redact_topics=[]):
    redacted_text = text
    redact_settings = {
        "PERSON": redact_names,
        "DATE": redact_dates,
        "PHONE": redact_phones,
        "ADDRESS": redact_address,
    }

    for entity_type, should_redact in redact_settings.items():
        if should_redact and entity_type in entities:
            for item in entities[entity_type]:
                if item:
                    redacted_text = redacted_text.replace(item, '█' * len(item))

    if redact_topics:
        redacted_text = hide_terms_in_sentences(redacted_text, redact_topics)

    return redacted_text


def list_files(folder_pattern):
    import glob
    return glob.glob(folder_pattern)

def get_related_words(concept):
    from nltk.corpus import wordnet
    synonyms = []
    for syn in wordnet.synsets(concept):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name().replace('_', ' '))
    return list(set(synonyms))

def hide_terms_in_sentences(text, related_words):
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in related_words) + r')\b'
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    redacted_sentences = []

    for sentence in sentences:
        if re.search(pattern, sentence, re.IGNORECASE):
            redacted_sentences.append('█' * len(sentence))
        else:
            redacted_sentences.append(sentence)

    return ' '.join(redacted_sentences)
