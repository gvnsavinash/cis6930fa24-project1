import os
import argparse
import sys
import warnings
from assignment1.regex_helper import regex_match
from assignment1.utility_helpers import (
    merge_overlapping_substrings,
    redact,
    get_files_in_folder,
    find_concept_synonyms,
    censor_concept_terms,
)

def censor(text_input, ner_pipeline, concepts=None):
    """
    Censors sensitive information from a given text input using both regex and Hugging Face transformers.

    Args:
        text_input (str): The text to be processed.
        ner_pipeline: The Hugging Face NER pipeline.
        concepts (list): List of concepts to redact, if provided.

    Returns:
        dict: A dictionary containing the combined entities extracted from both regex and NER.
    """
    # If text_input is a file, read it line by line to preserve structure
    if os.path.exists(text_input):
        with open(text_input, 'r', encoding='utf-8') as f:
            content_lines = f.readlines()  # Keep the newline characters intact
    else:
        content_lines = text_input.splitlines()  # Handle multi-line input text

    # Join lines to form the full content for regex/NER processing
    content = "\n".join(content_lines)

    # Step 1: Use Regex to extract entities
    dict_regex_ent = regex_match(content)
    print("\n--- Regex Extraction ---")
    for key, value in dict_regex_ent.items():
        print(f"Regex extracted {len(value)} {key} entities: {value}")

    # Step 2: Use Hugging Face NER to extract additional entities
    ner_results = ner_pipeline(content)
    dict_hf_ent = {"PERSON": [], "DATE": [], "PHONE": [], "ADDRESS": [], "EMAIL": []}

    for entity in ner_results:
        if entity['entity_group'] == 'PER':
            dict_hf_ent['PERSON'].append(entity['word'])
        elif entity['entity_group'] == 'LOC':
            dict_hf_ent['ADDRESS'].append(entity['word'])
        elif entity['entity_group'] == 'DATE':
            dict_hf_ent['DATE'].append(entity['word'])

    # Step 2.5: Filter out PERSON entities that don't start with a capital letter
    dict_hf_ent['PERSON'] = [person for person in dict_hf_ent['PERSON'] if person[0].isupper()]
    
    print("\n--- Hugging Face NER Extraction ---")
    for key, value in dict_hf_ent.items():
        print(f"Transformers extracted {len(value)} {key} entities: {value}")

    # Step 3: Combine regex and NER results (union of both)
    for key in dict_regex_ent:
        if key in dict_hf_ent:
            dict_hf_ent[key].extend(dict_regex_ent[key])

    # Remove duplicates
    for key in dict_hf_ent:
        dict_hf_ent[key] = list(set(dict_hf_ent[key]))

    # Step 4: Handle concept redaction (Redact entire sentences if concept terms are present)
    if concepts:
        for concept in concepts:
            related_terms = find_concept_synonyms(concept)
            print(f"Related terms for concepts [{concept}]: {related_terms}")
            content = censor_concept_terms(content, related_terms)

    # Log the combined result before redaction
    print("\n--- Combined Extraction (Regex + NER) ---")
    for key, value in dict_hf_ent.items():
        print(f"Total combined {key} entities: {len(value)} - {value}")

    # Step 5: Redact sensitive information
    redacted_lines = []
    for line in content_lines:
        redacted_line = redact(
            line, 
            dict_hf_ent, 
            redact_names=args.names, 
            redact_dates=args.dates, 
            redact_phones=args.phones, 
            redact_address=args.address, 
            redact_concepts=concepts
        )  # Redact each line while preserving structure
        redacted_lines.append(redacted_line)

    return "\n".join(redacted_lines)  # Return the censored text with newlines intact


def main(args):
    """
    Main function of the redactor script using Hugging Face transformers and regex matching for entity recognition.

    Args:
        args: Command-line arguments.
    """
    warnings.filterwarnings("ignore", message="Some weights of the model checkpoint at dbmdz/bert-large-cased-finetuned-conll03-english were not used when initializing BertForTokenClassification: ['bert.pooler.dense.bias', 'bert.pooler.dense.weight'] - This IS expected.")
    
    # Load Hugging Face's NER pipeline with a model fine-tuned for NER tasks
    from transformers import pipeline
    ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

    files = get_files_in_folder(args.input)

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    import nltk
    nltk.download('wordnet')

    # Handle all text files in the folder
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            original_text = f.read()

        dict_ent = censor(original_text, ner_pipeline, concepts=args.concept)
        file_base = os.path.basename(file)

        # Write the redacted file with proper formatting
        with open(os.path.join(args.output, file_base + ".censored"), "w", encoding="utf-8") as f:
            f.write(dict_ent)

        print(f"File {file_base} processed and saved to {args.output}")

        # Print statistics (if required)
        if args.stats == "stderr":
            sys.stderr.write(f"Stats for {file}:\n")
        elif args.stats == "stdout":
            sys.stdout.write(f"Stats for {file}:\n")
        else:
            with open(args.stats, "w", encoding="utf-8") as f:
                f.write(f"Stats for {file}:\n")


if __name__ == "__main__":
    import logging

    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(name)s - %(level)s - %(message)s",
    #     datefmt="%m/%d/%Y %H:%M:%S",
    #     filename="tests/assignment1.log",
    #     filemode="a",
    # )

    # Command-line argument parser
    parser = argparse.ArgumentParser(description="Censor text files.")
    parser.add_argument("--input", help="Input file pattern", required=False, default="text_files/*.txt")
    parser.add_argument("--names", action="store_true", help="Censor names")
    parser.add_argument("--dates", action="store_true", help="Censor dates")
    parser.add_argument("--phones", action="store_true", help="Censor phone numbers")
    parser.add_argument("--address", action="store_true", help="Censor addresses")
    parser.add_argument("--concept", nargs="*", help="Concept terms to censor")
    parser.add_argument("--output", help="Output directory", required=False, default="files/")
    parser.add_argument("--stats", default="stdout", help="Statistics output destination")

    args = parser.parse_args()

    logging.info("Starting main")
    main(args)
    logging.info("Main ended")
