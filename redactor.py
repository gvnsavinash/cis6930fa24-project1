import os
import argparse
import sys
import warnings
import pyap
import spacy
from assignment1.pattern_matcher import *
from assignment1.helper import *
import us
import pycountry


nlp = spacy.load("en_core_web_md")

def find_addresses_with_pyap(text):
    found_addresses = pyap.parse(text, country='US')
    #print(f"i am in find_addresses_with_pyap Found addresses: {found_addresses}")
    return [str(address) for address in found_addresses]



def print_debug_info(stage, names=None, dates=None, phones=None, addresses=None):
    """Prints debug information for each stage of extraction."""
    print(f"\n--- {stage} ---")
    if names is not None:
        print(f"Persons: {names}")
    if dates is not None:
        print(f"Dates: {dates}")
    if phones is not None:
        print(f"Phones: {phones}")
    if addresses is not None:
        print(f"Addresses: {addresses}")

def format_entity_stats(file, args, names, dates, phones, addresses):
    stats_output = f"File: {file}\nEntity type : Number of occurrences\n\n"
    
    if args.names:
        stats_output += f"PERSON : {len(names)}\n"
    if args.dates:
        stats_output += f"DATE : {len(dates)}\n"
    if args.phones:
        stats_output += f"PHONE : {len(phones)}\n"
    if args.address:
        stats_output += f"ADDRESS : {len(addresses)}\n"
    
    stats_output += "\n"
    return stats_output

def redact_sensitive_info(text_input, args, topics=None):
    if os.path.exists(text_input):
        with open(text_input, 'r', encoding='utf-8') as f:
            lines_in_text = f.readlines()
    else:
        lines_in_text = text_input.splitlines()

    full_text = "\n".join(lines_in_text)

    
   

    # Step 1: Extract entities using regex
    regex_results = extract_using_regex(full_text)
    found_names = []
    found_dates = regex_results.get("DATE", [])
    found_phones = regex_results.get("PHONE", [])
    found_addresses = regex_results.get("ADDRESS", [])

    found_emails = regex_results.get("EMAIL", [])

    # Extract local parts of emails as names
    email_names = [email.split('@')[0] for email in found_emails]
    found_names.extend(email_names)

    names_from_titles = extract_titles_and_names(full_text)
    found_names.extend(names_from_titles)

    print_debug_info("Regex Extraction", names=found_names, dates=found_dates, phones=found_phones, addresses=found_addresses)

    # Step 2: Extract entities using SpaCy
    state_abbrs = [state.abbr for state in us.states.STATES]   
    state_names = [state.name for state in us.states.STATES] 
    countries_names = [country.name for country in pycountry.countries]
    countries_names_code = [country.alpha_2 for country in pycountry.countries]
    #print(f"State abbreviations: {state_abbrs}")

    spacy_names, spacy_dates, spacy_addresses = [], [], []
    doc = nlp(full_text)
    for entity in doc.ents:
        #print(f"Entity: {entity.text}, Label: {entity.label_}")
        if entity.label_ == 'GPE' :
            spacy_addresses.append(entity.text)
        elif entity.label_ == 'PERSON':
            spacy_names.append(entity.text)
        # elif entity.label_ == 'DATE':
        #     spacy_dates.append(entity.text)
        
    tokens = full_text.split()  # Split text into individual whitespace-separated tokens
    for token in tokens:
        token_normalized = token.strip('.,')  # Normalize tokens by removing punctuation like commas and periods
        if token_normalized in state_abbrs and len(token_normalized) == 2:
            spacy_addresses.append(token_normalized)
        elif token_normalized in state_names or token_normalized in countries_names or token_normalized in countries_names_code or token_normalized == 'USA':
            spacy_addresses.append(token_normalized)

    print_debug_info("SpaCy NER Extraction", names=spacy_names, dates=spacy_dates, addresses=spacy_addresses)

    # Step 3: Combine regex and SpaCy results, removing duplicates
    combined_names = list(set(found_names + spacy_names))
    combined_dates = list(set(found_dates + spacy_dates))
    combined_phones = list(set(found_phones))
    combined_addresses = list(set(found_addresses + spacy_addresses))

    print_debug_info("Combined Extraction (Regex + NER + pyap)", names=combined_names, dates=combined_dates, phones=combined_phones, addresses=combined_addresses)

    # Redact terms based on topics if specified
    if topics:
        for topic in topics:
            related_words = get_related_words(topic)
            full_text = hide_terms_in_sentences(full_text, related_words)

    # Step 4: Apply redaction
    redacted_text_lines = []
    for line in lines_in_text:
        pyap_addresses = find_addresses_with_pyap(line)
        if pyap_addresses:
            for address in pyap_addresses:
                #print(f"Found address: {address}")
                line = line.replace(address, '█' * len(address))

        redacted_line = apply_redaction(
            line,
            {"PERSON": combined_names, "DATE": combined_dates, "PHONE": combined_phones, "ADDRESS": combined_addresses},
            redact_names=args.names,
            redact_dates=args.dates,
            redact_phones=args.phones,
            redact_address=args.address,
            redact_topics=topics,
        )
        redacted_text_lines.append(redacted_line)

    return "\n".join(redacted_text_lines), combined_names, combined_dates, combined_phones, combined_addresses



def extract_titles_and_names(text):
    title_name_pattern = re.compile(
        r'\b(Dear|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+'  
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*'  
        r'(Jr\.|Sr\.|III|IV)?\b',  
        re.IGNORECASE
    )
    
    title_name_matches = title_name_pattern.findall(text)
    
    names_from_titles = [' '.join(filter(None, match[1:])).strip() for match in title_name_matches]
    return names_from_titles


def main(args):
    warnings.filterwarnings("ignore")
    files_to_process = list_files(args.input)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    import nltk
    nltk.download('wordnet')

    


    # Process each file and generate a unique stats file for each
    for i, file_path in enumerate(files_to_process, start=1):
        with open(file_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        # Redact information and extract entity stats
        redacted_content, names, dates, phones, addresses = redact_sensitive_info(original_text, args, topics=args.concept)
        file_name = os.path.basename(file_path)

        # Save the redacted content to a uniquely named file in the output directory
        with open(os.path.join(args.output, file_name + ".censored"), "w", encoding="utf-8") as f:
            f.write(redacted_content)

        print(f"File '{file_name}' processed and saved to '{args.output}'")

        # Define a unique name for each stats file (e.g., sample_stats1.txt, sample_stats2.txt)
        stats_file_path = os.path.join(args.output, f"sample_stats{i}.txt")
        
        # Format and save statistics to the uniquely named stats file
        stats_output = format_entity_stats(file_name, args, names, dates, phones, addresses)
        with open(stats_file_path, "w", encoding="utf-8") as stats_file:
            stats_file.write(stats_output)

        # Print statistics to stderr or stdout as specified
        if args.stats == "stderr":
            sys.stderr.write("Printing stats to stderr\n")
            sys.stderr.write(stats_output)
        elif args.stats == "stdout":
            sys.stdout.write("Printing stats to stdout\n")
            sys.stdout.write(stats_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact sensitive information from text files.")
    parser.add_argument("--input", help="Input file pattern", required=False, default="text_files/*.txt")
    parser.add_argument("--names", action="store_true", help="Redact names")
    parser.add_argument("--dates", action="store_true", help="Redact dates")
    parser.add_argument("--phones", action="store_true", help="Redact phone numbers")
    parser.add_argument("--address", action="store_true", help="Redact addresses")
    parser.add_argument("--concept", nargs="*", help="Topics to redact")
    parser.add_argument("--output", help="Output directory", required=False, default="files/")
    parser.add_argument("--stats", default="stdout", help="Output for statistics")

    args = parser.parse_args()

    main(args)
