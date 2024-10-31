import os
import argparse
import sys
import warnings
import pyap
import re
import spacy
from assignment1.pattern_matcher import *
from assignment1.helper import *
import us
import pycountry
import logging

# Set up the logging to record debug information to 'docs/codelogger.log'.
logging.basicConfig(filename='docs/codelogger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
import nltk
nltk.download('wordnet')

# Load the Spacy NLP model.
nlp = spacy.load("en_core_web_md")

# Function to find US addresses in text using the Pyap library.
def find_addresses_with_pyap(text):
    """
    Finds and returns addresses from the given text using the pyap library.

    This function parses the input text to identify addresses based on the 
    specified country (default is 'US'). It logs the found addresses for 
    debugging purposes and returns them as a list of strings.

    Args:
        text (str): The input text from which to extract addresses.

    Returns:
        list of str: A list of addresses found in the input text.
    """
    found_addresses = pyap.parse(text, country='US')
    logging.debug(f"Found addresses with pyap: {found_addresses}")
    return [str(address) for address in found_addresses]

# Function to print and log extraction details at various stages.
def print_debug_info(stage, names=None, dates=None, phones=None, addresses=None):
    """
    Prints and logs debug information for different stages of processing.

    Parameters:
    stage (str): The current stage of processing.
    names (list, optional): A list of names to be printed and logged. Defaults to None.
    dates (list, optional): A list of dates to be printed and logged. Defaults to None.
    phones (list, optional): A list of phone numbers to be printed and logged. Defaults to None.
    addresses (list, optional): A list of addresses to be printed and logged. Defaults to None.

    This function prints the provided information to the console and logs it using the logging module.
    """
    print(f"\n--- {stage} ---")
    logging.debug(f"Stage: {stage}")
    if names is not None:
        print(f"Persons: {names}")
        logging.debug(f"Persons: {names}")
    if dates is not None:
        print(f"Dates: {dates}")
        logging.debug(f"Dates: {dates}")
    if phones is not None:
        print(f"Phones: {phones}")
        logging.debug(f"Phones: {phones}")
    if addresses is not None:
        print(f"Addresses: {addresses}")
        logging.debug(f"Addresses: {addresses}")

# Function to format and log statistics about the redaction process.
def format_entity_stats(file, args, names, dates, phones, addresses):
    """
    Formats and returns a string containing statistics about different types of entities found in a file.

    Args:
        file (str): The name of the file being processed.
        args (Namespace): A namespace containing boolean flags indicating which entity types to include in the stats.
        names (list): A list of detected names (PERSON entities).
        dates (list): A list of detected dates (DATE entities).
        phones (list): A list of detected phone numbers (PHONE entities).
        addresses (list): A list of detected addresses (ADDRESS entities).

    Returns:
        str: A formatted string with the file name and the number of occurrences for each specified entity type.
    """
    stats_output = f"File: {file}\nEntity type : Number of occurrences\n\n"
    logging.info(f"Formatting stats for file: {file}")
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

# Main function to redact sensitive information based on specified arguments.
def redact_sensitive_info(text_input, args, topics=None):
    """
    Redacts sensitive information from the given text input based on specified arguments.
    Parameters:
    text_input (str): The input text or file path containing the text to be redacted.
    args (Namespace): Arguments specifying which types of information to redact (names, dates, phones, addresses).
    topics (list, optional): List of topics for additional redaction. Defaults to None.
    Returns:
    tuple: A tuple containing the redacted text, and lists of found names, dates, phones, and addresses.
    The function performs the following steps:
    1. Reads the input text from a file or directly from the provided string.
    2. Uses regex to extract names, dates, phone numbers, addresses, and emails.
    3. Extracts names from email addresses and titles.
    4. Uses SpaCy NLP to extract geographical and personal names.
    5. Normalizes tokens to identify additional addresses.
    6. Combines results from regex and SpaCy extractions.
    7. Optionally processes topics for redaction.
    8. Applies redaction to each line in the text based on the specified arguments.
    Debug information is printed at various stages to aid in tracing the extraction and redaction process.
    """
    # Open file if path exists or split input text into lines.
    if os.path.exists(text_input):
        with open(text_input, 'r', encoding='utf-8') as f:
            lines_in_text = f.readlines()
    else:
        lines_in_text = text_input.splitlines()

    full_text = "\n".join(lines_in_text)

    # Perform regex-based extraction of entities.
    regex_results = extract_using_regex(full_text)
    found_names, found_dates, found_phones, found_addresses, found_emails = [], regex_results.get("DATE", []), regex_results.get("PHONE", []), regex_results.get("ADDRESS", []), regex_results.get("EMAIL", [])

    # Extract names from emails and add to the list of found names.
    email_names = [email.split('@')[0] for email in found_emails]
    found_names.extend(email_names)

    # Extract names based on titles like 'Mr.', 'Ms.', etc.
    names_from_titles = extract_titles_and_names(full_text)
    found_names.extend(names_from_titles)

    # Debug information after regex extraction.
    #print_debug_info("Regex Extraction", names=found_names, dates=found_dates, phones=found_phones, addresses=found_addresses)

    # Prepare location data for further entity extraction.
    state_abbrs = [state.abbr for state in us.states.STATES]   
    state_names = [state.name for state in us.states.STATES] 
    countries_names = [country.name for country in pycountry.countries]
    countries_names_code = [country.alpha_2 for country in pycountry.countries]

    # Use Spacy NLP to extract names and addresses.
    spacy_names, spacy_dates, spacy_addresses = [], [], []
    doc = nlp(full_text)
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            spacy_addresses.append(entity.text)
        elif entity.label_ == 'PERSON':
            spacy_names.append(entity.text)

    # Normalize and check tokens for additional addresses.
    tokens = full_text.split()
    for token in tokens:
        token_normalized = token.strip('.,')
        if token_normalized in state_abbrs and len(token_normalized) == 2:
            spacy_addresses.append(token_normalized)
        elif token_normalized in state_names or token_normalized in countries_names or token_normalized in countries_names_code or token_normalized == 'USA':
            spacy_addresses.append(token_normalized)

    # Debug information after SpaCy NER extraction.
    #print_debug_info("SpaCy NER Extraction", names=spacy_names, dates=spacy_dates, addresses=spacy_addresses)

    # Combine names, dates, phones, and addresses from both extraction methods.
    combined_names = list(set(found_names + spacy_names))
    combined_dates = list(set(found_dates + spacy_dates))
    combined_phones = list(set(found_phones))
    combined_addresses = list(set(found_addresses + spacy_addresses))

    # Debug information after combining results from all extraction methods.
    #print_debug_info("Combined Extraction (Regex + NER + pyap)", names=combined_names, dates=combined_dates, phones=combined_phones, addresses=combined_addresses)

    # Process topics for redaction if specified.
    if topics is not None:
        from pandas.core.common import flatten
        topics = list(flatten([get_related_words(topic) for topic in topics]))

    # Apply redaction to each line in the text.
    redacted_text_lines = []
    for line in lines_in_text:
        if args.address:
            pyap_addresses = find_addresses_with_pyap(line)
            if pyap_addresses:
                for address in pyap_addresses:
                    line = line.replace(address, '█' * len(address))

        redacted_line = apply_redaction(
            line,
            {"PERSON": combined_names, "DATE": combined_dates, "PHONE": combined_phones, "ADDRESS": combined_addresses},
            redact_names=args.names,
            redact_dates=args.dates,
            redact_phones=args.phones,
            redact_address=args.address,
            redact_topics=topics
        )
        redacted_text_lines.append(redacted_line)

    return "\n".join(redacted_text_lines), combined_names, combined_dates, combined_phones, combined_addresses

# Function to extract names based on titles from the text.
def extract_titles_and_names(text):
    """
    Extracts titles and names from the given text.
    This function searches for patterns in the text that match common titles 
    (e.g., Dear, Mr., Mrs., Ms., Dr., Prof.) followed by a name. It captures 
    the title, the name, and any suffix (e.g., Jr., Sr., III, IV). The names 
    are then extracted and returned as a list.
    Args:
        text (str): The input text from which to extract titles and names.
    Returns:
        list: A list of names extracted from the text, excluding the titles.
    """
    title_name_pattern = re.compile(
        r'\b(Dear|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+'  
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*'  
        r'(Jr\.|Sr\.|III|IV)?\b',  
        re.IGNORECASE
    )
    
    title_name_matches = title_name_pattern.findall(text)
    
    names_from_titles = [' '.join(filter(None, match[1:])).strip() for match in title_name_matches]
    logging.debug(f"Extracted names from titles: {names_from_titles}")
    return names_from_titles

# Main function to process files and apply redactions.
def main(args):
    """
    Main function to process and redact sensitive information from files.
    Args:
        args (Namespace): Command-line arguments containing input directory, output directory,
                          redaction options, and stats output preferences.
    Workflow:
        1. Suppresses warnings.
        2. Lists files to process from the input directory.
        3. Creates the output directory if it doesn't exist.
        4. For each file:
            a. Reads the file content.
            b. Redacts sensitive information (names, dates, phones, addresses, and topics).
            c. Saves the redacted content to the output directory with a ".censored" extension.
            d. Logs the processing status.
            e. Generates and saves statistics about the redacted entities.
            f. Optionally prints statistics to stderr or stdout based on user preference.
    """
    warnings.filterwarnings("ignore")
    files_to_process = list_files(args.input)

    # Create output directory if it doesn't exist.
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    # Process each file, apply redactions, and save the results.
    for i, file_path in enumerate(files_to_process, start=1):
        with open(file_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        redacted_content, names, dates, phones, addresses = redact_sensitive_info(original_text, args, topics=args.concept)
        file_name = os.path.basename(file_path)

        with open(os.path.join(args.output, file_name + ".censored"), "w", encoding="utf-8") as f:
            f.write(redacted_content)

        logging.info(f"File '{file_name}' processed and saved to '{args.output}'")

        stats_file_path = os.path.join(args.output, f"sample_stats{i}.txt")
        
        stats_output = format_entity_stats(file_name, args, names, dates, phones, addresses)
        with open(stats_file_path, "w", encoding="utf-8") as stats_file:
            stats_file.write(stats_output)

        # if args.stats == "stderr":
        #     sys.stderr.write("Printing stats to stderr\n")
        #     sys.stderr.write(stats_output)
        # elif args.stats == "stdout":
        #     sys.stdout.write("Printing stats to stdout\n")
        #     sys.stdout.write(stats_output)


        

# Argument parsing and main function call.
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
