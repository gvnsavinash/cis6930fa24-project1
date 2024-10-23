import os
import re

def merge_overlapping_substrings(entity_list):
    """
    Merges overlapping or consecutive substrings in the entity list.
    
    Args:
        entity_list (list): A list of strings representing entities to be merged if they overlap.
    
    Returns:
        list: A list of merged entities.
    """
    if not entity_list:
        return []

    # Sort entities by their length in reverse order
    sorted_entities = sorted(entity_list, key=len, reverse=True)

    merged_entities = []
    for entity in sorted_entities:
        if not merged_entities:
            merged_entities.append(entity)
        else:
            overlap_found = False
            for i, merged_entity in enumerate(merged_entities):
                if entity in merged_entity or merged_entity in entity:
                    overlap_found = True
                    merged_entities[i] = entity if len(entity) > len(merged_entity) else merged_entity
                    break

            if not overlap_found:
                merged_entities.append(entity)

    return merged_entities


def redact(text, entities, redact_names=False, redact_dates=False, redact_phones=False, redact_address=False, redact_concepts=[]):
    """
    Redact the text based on the entities and the specified flags for redaction.

    Args:
        text (str): The text to redact.
        entities (dict): A dictionary containing entity types and their extracted values.
        redact_names (bool): If True, redact names.
        redact_dates (bool): If True, redact dates.
        redact_phones (bool): If True, redact phone numbers.
        redact_address (bool): If True, redact addresses.
        redact_concepts (list): List of concept-related terms to redact.

    Returns:
        str: The redacted text.
    """
    redacted_text = text

    if redact_names and 'PERSON' in entities:
        for name in entities['PERSON']:
            redacted_text = redacted_text.replace(name, '█' * len(name))

    if redact_dates and 'DATE' in entities:
        for date in entities['DATE']:
            if isinstance(date, tuple):
                # Join the non-empty parts of the tuple
                date = ''.join(part for part in date if part)
            if date:
                redacted_text = redacted_text.replace(date, '█' * len(date))

    if redact_phones and 'PHONE' in entities:
        for phone in entities['PHONE']:
            redacted_text = redacted_text.replace(phone, '█' * len(phone))

    if redact_address and 'ADDRESS' in entities:
        for address in entities['ADDRESS']:
            redacted_text = redacted_text.replace(address, '█' * len(address))

    # Redact based on concepts
    if redact_concepts:
        redacted_text = censor_concept_terms(redacted_text, redact_concepts)

    return redacted_text

def get_files_in_folder(folder_pattern):
    """
    Retrieves the list of files in the folder based on the input pattern (e.g., '*.txt').

    Args:
        folder_pattern (str): The glob pattern for file selection.
    
    Returns:
        list: A list of file paths matching the input pattern.
    """
    import glob
    files = glob.glob(folder_pattern)
    return files


def find_concept_synonyms(concept):
    """
    Finds synonyms for the given concept using WordNet.

    Args:
        concept (str): The concept word to find synonyms for.

    Returns:
        list: A list of synonyms for the concept.
    """
    from nltk.corpus import wordnet
    synonyms = []
    for syn in wordnet.synsets(concept):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name().replace('_', ' '))
    return list(set(synonyms))


def censor_concept_terms1(text, related_terms):
    """
    Censor any word in the text that matches any of the related concept terms.

    Args:
        text (str): The original input text.
        related_terms (list): The list of concept-related terms to censor.

    Returns:
        str: The redacted text with concept-related words censored.
    """
    words = text.split()  # Split text into individual words

    # Iterate through each word and replace with a redacted version if it's in the related_terms
    redacted_words = []
    for word in words:
        # Check case-insensitive match with any term in the related_terms list
        if any(term.lower() == re.sub(r'[^\w\s]', '', word.lower()) for term in related_terms):
            redacted_words.append('█' * len(word))  # Redact the word with punctuation
            print(f"Redacting: {word}")
        else:
            redacted_words.append(word)  # Keep the word

    # Rebuild the redacted text from the redacted words
    print(f"Redacted text finialsed : {' '.join(redacted_words)}")
    return ' '.join(redacted_words)





import re

def censor_concept_terms(text, related_terms):
    """
    Censor any sentence in the text that contains any of the related concept terms.

    Args:
        text (str): The original input text.
        related_terms (list): The list of concept-related terms to censor.

    Returns:
        str: The redacted text with sentences containing concept-related words censored.
    """
    # Split the text into sentences using regular expressions to handle punctuation
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)  # Split at punctuation

    redacted_sentences = []
    
    # print(f"Original text: {text}")
    # print(f"Sentences identified: {len(sentences)}\n")
    
    for i, sentence in enumerate(sentences):
        #print(f"Processing sentence {i + 1}: {sentence}")
        
        # Check if any concept-related term is in the sentence (case-insensitive), allow trailing punctuation
        if any(re.search(rf'\b{re.escape(term)}[.,;!?]?\b', sentence, re.IGNORECASE) for term in related_terms):
            # Redact entire sentence if a term is found
            redacted_sentence = '█' * len(sentence)  # Full redaction of the sentence including spaces
            redacted_sentences.append(redacted_sentence)
            #print(f"Redacting sentence {i + 1}: {sentence}\n")
        else:
            redacted_sentences.append(sentence)  # Keep sentence unchanged if no concept is found
            #print(f"Keeping sentence {i + 1}: {sentence}\n")

    # Join the redacted sentences back into the full text
    redacted_text = ' '.join(redacted_sentences)
    #print(f"\nRedacted text finalized: {redacted_text}")
    return redacted_text
