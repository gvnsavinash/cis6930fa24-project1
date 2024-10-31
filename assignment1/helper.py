import os
import re
import logging

# Configure logger for helper.py
logging.basicConfig(filename='docs/codelogger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to apply redactions to text based on specified settings and entity lists.
def apply_redaction(text, entities, redact_names=False, redact_dates=False, redact_phones=False, redact_address=False, redact_topics=[] ):
    """
    Redacts specified types of sensitive information from the given text.
    Parameters:
    text (str): The input text to be redacted.
    entities (dict): A dictionary where keys are entity types (e.g., "PERSON", "DATE") and values are lists of entities to be redacted.
    redact_names (bool): If True, redact names (entities of type "PERSON"). Default is False.
    redact_dates (bool): If True, redact dates (entities of type "DATE"). Default is False.
    redact_phones (bool): If True, redact phone numbers (entities of type "PHONE"). Default is False.
    redact_address (bool): If True, redact addresses (entities of type "ADDRESS"). Default is False.
    redact_topics (list): A list of additional topics/terms to be redacted from the text.
    Returns:
    str: The redacted text with specified entities and topics replaced by a series of █ characters.
    """
    logging.debug("Applying redactions based on settings.")
    redacted_text = text  
    redact_settings = {
        "PERSON": redact_names,
        "DATE": redact_dates,
        "PHONE": redact_phones,
        "ADDRESS": redact_address,
    }
    #print(f"entites in redact {entities}")
    # Iterate over each entity type and apply redaction if enabled.
    for entity_type, should_redact in redact_settings.items():
        if should_redact and entity_type in entities:
            for item in entities[entity_type]:
                # pattern = r'\b' + re.escape(item) + r'\b'
                redacted_text = redacted_text.replace(item, '█' * len(item))
                # redacted_text = re.sub(pattern, '█' * len(item), redacted_text, flags=re.IGNORECASE)
                logging.debug(f"Redacted {entity_type}: {item}")
    # Additional redaction for specified topics.
    if redact_topics:
        redacted_text = hide_terms_in_sentences(redacted_text, redact_topics)
        logging.debug("Applied topic-based redactions.")

    return redacted_text

# Function to list files in a directory based on a glob pattern.
def list_files(folder_pattern):
    """
    Lists all files matching the given folder pattern.

    Args:
        folder_pattern (str): The pattern to match files against, using Unix shell-style wildcards.

    Returns:
        list: A list of file paths that match the given pattern.

    Example:
        files = list_files('/path/to/folder/*.txt')
        # This will return a list of all .txt files in the specified folder.
    """
    import glob
    files = glob.glob(folder_pattern)
    logging.debug(f"Listing files with pattern {folder_pattern}: {files}")
    return files

# Function to retrieve related words for a given concept using WordNet.
def get_related_words(concept):
    """
    Retrieve a list of words related to a given concept using WordNet.
    This function finds synonyms, hypernyms (more general terms), and hyponyms (more specific terms) 
    for the provided concept. It removes WordNet suffixes from the related words and ensures 
    uniqueness by converting the list to a set.
    Args:
        concept (str): The concept word for which related words are to be found.
    Returns:
        list: A list of unique related words for the given concept.
    Logs:
        Debug information about the related words found for the concept.
    """
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
    #print(f"Related words for concept {concept}: {synonyms}")
    return list(set(synonyms))

# Function to redact entire sentences containing any of a list of terms.
def hide_terms_in_sentences(text, related_words):
    """
    Redacts sentences in the given text that contain any of the related words.
    Args:
        text (str): The input text containing multiple sentences.
        related_words (list of str): A list of words to search for in the sentences.
    Returns:
        str: The text with sentences containing related words redacted.
    The function splits the input text into sentences, checks each sentence for the presence of any word from the related_words list (which we will get from the get_related_words function),
    and replaces the entire sentence with a redacted block if any related word is found. The redacted sentences are joined back into a single string.
    """
    sentences = re.split(r'\. ', text)
    redacted_sentences = []
    #print(f"related words n hide terms function {related_words, len(sentences)}")
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
            
            #print(f"Keeping a sentence: {word }, {sentence}")
            redacted_sentences.append(sentence + '.')
    final_text = ' '.join(redacted_sentences).rstrip('.')
    if text.endswith('.'):
        final_text += '.'
    logging.debug(f"Final redacted text: {final_text}")
    return final_text
