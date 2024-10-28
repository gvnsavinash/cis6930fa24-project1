import re

def extract_using_regex(text):
    # Common patterns
    months_long = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    months_short = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    weekdays_long = r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
    weekdays_short = r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
    upper = r'[A-Z]'  # Shorthand for uppercase letters
    lower = r'[a-z]'  # Shorthand for lowercase letters
    name = upper + lower + r'+'
    
    # Address components
    address_suffix = r'(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Lane|Ln|Drive|Dr|Plaza|Way|Terrace|Court|Square|Loop|Parkway|Str)'
    additional_info = r'(?:,?\s(?:\d+\s)?(?:[A-Za-z]+\s)?(?:Floor|Fl|Suite|Ste|Room|Apt|Unit|#)\s?\d+[A-Za-z]?)?'

    # Specific patterns using common elements
    patterns = {
        "PERSON": r'\b' + name + r'\s' + name + r'\b',
        "EMAIL": r'\b[A-Za-z0-9._%+-]+(?:/[A-Za-z0-9._%+-]+)*@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "PHONE": r'(?<!\d)(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?![\d.])',
        "ADDRESS": (
            r'\b\d+\s(?:[A-Za-z]+\s?)+'
            + address_suffix +
            r'\b' + additional_info +
            r'(?:,?\s(?:[A-Za-z]+\s)+,?\s?' + upper + r'{2}\s?\d{5}(?:-\d{4})?)?'
        ),
        "DATE": (
            r'\b\d{1,2}(?:st|nd|rd|th)?\s' + months_long + r'\s\d{4}\b'  # e.g., 12th April 2023
            r'|\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b'  # e.g., 12/04/2023 or 12-04-2023
            r'|\b' + weekdays_long + r',\s\d{1,2}\s' + months_short + r'\s\d{1,2}(?:st|nd|rd|th)?,\s\d{4}\b'  # e.g., Monday, 12 Apr 2023
            r'|\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b'  # e.g., 2023/04/12
            r'|\b' + months_long + r'\s\d{1,2},\s\d{4}\b'  # e.g., April 12, 2023
            r'|\b' + months_long + r'\s\d{4}\b'  # e.g., April 2023
            r'|\b' + weekdays_short + r',\s\d{1,2}\s' + months_short + r'\s\d{4}\b'  # e.g., Mon, 12 Apr 2023
            r'|\b' + weekdays_long + r',\s' + months_long + r'\s\d{1,2}(?:st|nd|rd|th),\s\d{4}\b'  # e.g., Monday, April 12th, 2023
        )
    }

    # Extracting and returning the results
    results = {key: re.findall(pattern, text) for key, pattern in patterns.items()}
    return results



