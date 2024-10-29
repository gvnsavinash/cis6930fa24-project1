import os
import re
import logging

# Configure logger for helper.py
logging.basicConfig(filename='docs/codelogger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def apply_redaction(text, entities, redact_names=False, redact_dates=False, redact_phones=False, redact_address=False, redact_topics=[]):
    logging.debug("Applying redactions based on settings.")
    redacted_text = text  
    redact_settings = {
        "PERSON": redact_names,
        "DATE": redact_dates,
        "PHONE": redact_phones,
        "ADDRESS": redact_address,
    }
    #print(f"entites in redact {entities}")
    for entity_type, should_redact in redact_settings.items():
        if should_redact and entity_type in entities:
            for item in entities[entity_type]:
                # pattern = r'\b' + re.escape(item) + r'\b'
                redacted_text = redacted_text.replace(item, '█' * len(item))
                # redacted_text = re.sub(pattern, '█' * len(item), redacted_text, flags=re.IGNORECASE)
                logging.debug(f"Redacted {entity_type}: {item}")

    if redact_topics:
        redacted_text = hide_terms_in_sentences(redacted_text, redact_topics)
        logging.debug("Applied topic-based redactions.")

    return redacted_text

def list_files(folder_pattern):
    import glob
    files = glob.glob(folder_pattern)
    logging.debug(f"Listing files with pattern {folder_pattern}: {files}")
    return files

def get_related_words(concept):
    from nltk.corpus import wordnet
    synonyms = []
    for syn in wordnet.synsets(concept):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name().replace('_', ' '))
        for lemma in syn.hypernyms():
            # Remove WordNet suffixes like '.n.01' or '.v.01'
            clean_name = re.sub(r'\.\w\.\d+', '', lemma.name().replace('_', ' '))
            synonyms.append(clean_name)
        for lemma in syn.hyponyms():
            clean_name = re.sub(r'\.\w\.\d+', '', lemma.name().replace('_', ' '))
            synonyms.append(clean_name)
    synonyms =set(synonyms)

    logging.debug(f"Related words for concept {concept}: {synonyms}")
    print(f"Related words for concept {concept}: {synonyms}")
    return list(set(synonyms))

def hide_terms_in_sentences(text, related_words):
    sentences = re.split(r'\. ', text)
    redacted_sentences = []
    print(f"related words n hide terms function {related_words, len(sentences)}")
    for sentence in sentences:
        should_redact = False
        for word in related_words:
            if word.lower() in sentence.lower():
                should_redact = True
                break
        if should_redact:
            redacted_sentences.append('█' * len(sentence))
            # print(f"Redacted a sentence due to related word: {sentence}")
            logging.debug(f"Redacted a sentence due to related word: {sentence}")
        else:
            
            print(f"Keeping a sentence: {word }, {sentence}")
            redacted_sentences.append(sentence + '.')
    final_text = ' '.join(redacted_sentences).rstrip('.')
    if text.endswith('.'):
        final_text += '.'
    logging.debug(f"Final redacted text: {final_text}")
    return final_text
