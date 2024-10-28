import re

def regex_match(text_input):
    """
    Matches sensitive information in the text using generalized regex patterns for person names, emails, phone numbers,
    addresses, SSNs, dates, and other sensitive categories (income, medical info, login credentials).

    Args:
        text_input (str): The input text.

    Returns:
        dict: A dictionary containing the matched entities using regex patterns:
            - "PERSON": List of matched person names.
            - "EMAIL": List of matched email addresses.
            - "PHONE": List of matched phone numbers.
            - "ADDRESS": List of matched addresses.
            - "DATE": List of matched dates.
            - "SSN": List of matched SSNs.
            - "LOGIN": List of matched login credentials.
            
    """
    # Updated regex patterns for each category
    #person_pattern = re.compile(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b")  # Full name pattern
    person_pattern = re.compile(r'\b([A-Z][a-z]+\.[A-Z][a-z]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')

    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')  # Email pattern
    phone_pattern = re.compile(
    r'(?<!\d)'                               # No digit before
    r'(?:\+?\d{1,3}[-.\s]?)?'                # Optional country code with 1-3 digits
    r'\(?\d{3}\)?[-.\s]?'                    # Area code with exactly 3 digits, optional parentheses
    r'\d{3}[-.\s]?\d{4}'                     # Main number in 3-4 digit format
    r'(?![\d.])'                             # No digit or decimal after
)
    address_pattern = re.compile(r'\d+\s(?:[A-Za-z]+\s?)+(?:St|Street|Ave|Avenue|Blvd|Rd|Road|Lane|Ln|Drive|Dr)\b')  # Addresses
 



    date_pattern = re.compile(
    r'(?:\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b)'                    # MM/DD/YYYY, DD/MM/YYYY, or short forms
    r'|(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2},\s\d{4}\b)'  # Month Day, Year with comma
    r'|(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}\b)'  # Month Year (e.g., March 2024)
    r'|(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}\b)'  # Month Day without year
    r'|(?:\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b)'                     # ISO format YYYY-MM-DD
    r'|(?:\b\d{1,2}[-/]\d{1,2}[-/]\d{2}\b)'                     # Short year format MM/DD/YY, DD/MM/YY
    r'|(?:\b\w{3},\s\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{4}\b)'  # Day, DD Month YYYY
    r'|(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s?\n\s?\d{1,2}\b)'  # Month with line break before day
)



    
    
    
    # Create the dictionary to hold extracted entities
    dict_regex_ent = {
        "PERSON": re.findall(person_pattern, text_input),
        "EMAIL": re.findall(email_pattern, text_input),
        "PHONE": re.findall(phone_pattern, text_input),
        "ADDRESS": re.findall(address_pattern, text_input),
        "DATE": re.findall(date_pattern, text_input),
        
        
        
    }

    return dict_regex_ent 