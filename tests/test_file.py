
import os.path
import sys
import pytest

from assignment1.helper import *
from assignment1.pattern_matcher import *
from redactor import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assignment1')))



def test_extract_using_regex():
    """
    Test the extract_using_regex function.

    This test case verifies that the extract_using_regex function correctly extracts
    specific information from a given text using regular expressions. The text contains
    a person's name, an email address, and a phone number. The function is expected to
    return a dictionary with keys 'EMAIL', 'PHONE', and 'PERSON', each containing the
    corresponding extracted values.

    Assertions:
    - The extracted email address should be 'grant@gmail.com'.
    - The extracted phone number should be '658-856-4967'.
    - The extracted person's name should be 'Venkata Avinash'.

    Raises:
    - AssertionError: If any of the expected values are not found in the result.
    """
    text = "Venkata Avinash met Grant  on October 28th, 2024. They talked each other and Grant gave his contact detail's as grant@gmail.com and number is 658-856-4967 , Thanks ."
    result = extract_using_regex(text)
    assert 'grant@gmail.com' in result['EMAIL']
    assert '658-856-4967' in result['PHONE']
    assert 'Venkata Avinash' in result['PERSON']
    
def test_apply_redaction():
    """
    Test the apply_redaction function to ensure it correctly redacts specified entities in a given text based on Spacy (NLP).

    This test checks if the function can successfully redact names and addresses from the input text.
    
    Test Case:
    - Input text: "Contact Avinash at Florida."
    - Entities to redact: {'PERSON': ['Avinash'], 'ADDRESS': ['Florida']}
    - Redaction flags: redact_names=True, redact_address=True
    
    Asserts:
    - The redacted text contains the redaction character '█'.
    """
    text = "Contact Avinash at Florida."
    entities = {'PERSON': ['Avinash'], 'ADDRESS': ['Florida']}
    redacted_text = apply_redaction(text, entities, redact_names=True, redact_address=True)
    assert '█' in redacted_text

def test_list_files():
    """
    Tests the list_files function to ensure it returns a list of Python files.

    This test checks if the list_files function correctly identifies and returns
    a list of files matching the specified folder pattern. The folder pattern used
    in this test is "*.py", which should match all Python files. The test asserts
    that the returned value is a list and that all elements in the list end with
    the ".py" extension.
    """
    folder_pattern = "*.py"
    files = list_files(folder_pattern)
    assert isinstance(files, list) and all(f.endswith('.py') for f in files)



def test_get_related_words():
    """
    Test the get_related_words function.

    This test checks if the get_related_words function returns a list of related words
    for a given concept. Specifically, it verifies that the returned value is a list
    and that the word 'phone' is included in the list of related words for the concept 'call'.
    """
    concept = "call"
    related_words = get_related_words(concept)
    assert isinstance(related_words, list) and 'phone' in related_words



def test_hide_terms_in_sentences():
    """
    Test the hide_terms_in_sentences function.

    This test checks if the hide_terms_in_sentences function correctly redacts
    the specified related words in the given text by replacing them with a 
    redaction character (e.g., '█').

    Test Case:
    - Input text: "The quick brown fox jumps over the lazy dog."
    - Related words to redact: ["fox", "dog"]
    - Expected behavior: The words "fox" and "dog" should be redacted in the 
        output text.

    Assertions:
    - The redacted text should contain the redaction character '█'.
    """
    text = "The quick brown fox jumps over the lazy dog."
    related_words = ["fox", "dog"]
    redacted_text = hide_terms_in_sentences(text, related_words)
    assert '█' in redacted_text















