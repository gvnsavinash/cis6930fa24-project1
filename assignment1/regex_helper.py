import re

def extract_using_regex(text):
    patterns = {
        "PERSON": r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',
        "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "PHONE": r'(?<!\d)(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?![\d.])',
        "ADDRESS": (
            r'\b\d+\s(?:[A-Za-z]+\s?)+(?:St|Street|Ave|Avenue|Blvd|Boulevard|Rd|Road|Lane|Ln|'
            r'Drive|Dr|Plaza|Way|Terrace|Court|Square|Loop|Parkway|Str)\b(?:,?\s(?:Unit\s\d+|'
            r'Apt\s\d+|Suite\s\d+|Unit\s\d+[A-Z])?)?(?:,\s?[A-Za-z\s]+)?,?\s?(?:[A-Z]{2}\s?\d{5}(?:-\d{4})?)?'
        ),
        "DATE": (
            r'(?:\b\d{1,2}(?:st|nd|rd|th)?\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|'
            r'May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)\s\d{4}\b)|(?:\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b)|(?:\b(?:Mon|'
            r'Tues|Wednes|Thurs|Fri|Satur|Sun)day,\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|'
            r'Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|'
            r'Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}(?:st|nd|rd|th)?,\s\d{4}\b)'
        )
    }

    results = {
        "PERSON": re.findall(patterns["PERSON"], text),
        "EMAIL": re.findall(patterns["EMAIL"], text),
        "PHONE": re.findall(patterns["PHONE"], text),
        "ADDRESS": re.findall(patterns["ADDRESS"], text),
        "DATE": re.findall(patterns["DATE"], text),
    }

    return results
