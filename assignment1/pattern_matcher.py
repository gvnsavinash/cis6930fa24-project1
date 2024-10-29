import re
import logging

# Configure logger for pattern_matcher.py
logging.basicConfig(filename='docs/codelogger.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_using_regex(text):
    logging.debug("Starting regex extraction of entities.")
    months_long = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    months_short = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    upper = r'[A-Z]'
    lower = r'[a-z]'
    name = upper + lower + r'+'
    
    address_suffix = r'(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Plaza|Way|Terrace|Court|Square|Loop|Parkway|Str)'
    additional_info = r'(?:,?\s(?:\d+\s)?(?:[A-Za-z]+\s)?(?:Floor|Fl|Suite|Ste|Room|Apt|Unit|#)\s?\d+[A-Za-z]?)?'

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

    results = {key: re.findall(pattern, text) for key, pattern in patterns.items()}
    logging.debug(f"Regex extraction results: {results}")
    return results
