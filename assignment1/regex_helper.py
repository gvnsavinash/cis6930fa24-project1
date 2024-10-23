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
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')  # Email pattern
    phone_pattern = re.compile(r'\+?\d{1,4}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,9}')  # Phone numbers
    address_pattern = re.compile(r'\d+\s(?:[A-Za-z]+\s?)+(?:St|Street|Ave|Avenue|Blvd|Rd|Road|Lane|Ln|Drive|Dr)\b')  # Addresses
    date_pattern = re.compile(r'(\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b)|(\b\w+\s\d{1,2}(?:th|rd|st)?,\s\d{4}\b)')  # Dates in MM/DD/YYYY or DD/MM/YYYY formats
    
    
    
    # Create the dictionary to hold extracted entities
    dict_regex_ent = {
        #"PERSON": re.findall(person_pattern, text_input),
        "EMAIL": re.findall(email_pattern, text_input),
        "PHONE": re.findall(phone_pattern, text_input),
        "ADDRESS": re.findall(address_pattern, text_input),
        "DATE": re.findall(date_pattern, text_input),
        
        
        
    }

    return dict_regex_ent
