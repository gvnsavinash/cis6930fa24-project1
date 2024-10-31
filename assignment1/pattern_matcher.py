import re
import logging

# Set up logging for this module.
logging.basicConfig(filename='docs/codelogger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract entities from text using regex patterns.
def extract_using_regex(text):
    """
    Extract entities from the given text using regular expressions.
    This function uses predefined regular expression patterns to identify and extract various types of entities 
    from the input text. The entities that can be extracted include:
    - PERSON: Full names consisting of a first name and a last name, both starting with an uppercase letter.
    - EMAIL: Email addresses following the standard email format.
    - PHONE: Phone numbers in various formats, including international formats.
    - ADDRESS: Street addresses with optional additional information like floor, suite, or apartment number.
    - DATE: Dates in multiple formats, including long-form dates (e.g., "March 14, 1879"), short-form dates 
      (e.g., "01/01/2020"), and day-month-year formats.
    Args:
        text (str): The input text from which entities are to be extracted.
    Returns:
        dict: A dictionary where the keys are entity types (e.g., "PERSON", "EMAIL") and the values are lists 
        of strings representing the extracted entities of that type.

    Example:
        --- text = "Albert Einstein was born on March 14, 1879. His email was einstein@theory.com and his phone number was +49 89 123456. He lived at 112 Mercer St, Princeton, NJ 08540."
        --- extract_using_regex(text)
        {
            'PERSON': ['Albert Einstein'],
            'EMAIL': ['einstein@theory.com'],
            'PHONE': ['+49 89 123456'],
            'ADDRESS': ['112 Mercer St, Princeton, NJ 08540'],
            'DATE': ['March 14, 1879']
        }
    
    """
    logging.debug("Starting regex extraction of entities.")
    
    # Define regex patterns for various entity types.
    months_long = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    months_short = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    upper = r'[A-Z]'
    lower = r'[a-z]'
    name = upper + lower + r'+'
    
    address_suffix = r'(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Plaza|Way|Terrace|Court|Square|Loop|Parkway|Str)'
    additional_info = r'(?:,?\s(?:\d+\s)?(?:[A-Za-z]+\s)?(?:Floor|Fl|Suite|Ste|Room|Apt|Unit|#)\s?\d+[A-Za-z]?)?'

    # Aggregate patterns for different entities.
    patterns = {
        "PERSON": r'\b' + name + r'\s' + name + r'\b',
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "PHONE": r'(?<!\d)(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?![\d.])',
        "ADDRESS": (
            r'\b\d+\s(?:[A-Za-z]+\s?)+' + address_suffix + r'\b' + additional_info +
            r'(?:,?\s(?:[A-Za-z]+\s)+,?\s?' + upper + r'{2}\s?\d{5}(?:-\d{4})?)?'
        ),
        "DATE": (
            r'\b\d{1,2}(?:st|nd|rd|th)?\s' + months_long + r'\s\d{4}\b'
            r'|\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b'
            r'|\b' + months_long + r'\s\d{1,2},\s\d{4}\b'
            r'|\b' + months_long + r' \d{1,2}\b'
            r'|\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s\d{1,2}\s' + months_short + r'\s\d{4}\b'
        )
    }

    # Extract entities using the defined patterns.
    results = {key: re.findall(pattern, text) for key, pattern in patterns.items()}
    logging.debug(f"Regex extraction results: {results}")
    return results
