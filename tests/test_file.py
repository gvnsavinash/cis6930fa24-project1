
import os.path
import sys
import pytest

from assignment1.helper import *
from assignment1.pattern_matcher import *
from redactor import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assignment1')))



def test_name():
    assert isinstance("Avinash", str)

def test_extract_using_regex():
    text = "Venkata Avinash met Grant  on October 28th, 2024. They talked each other and Grant gave his contact detail's as grant@gmail.com and number is 658-856-4967 , Thanks ."
    result = extract_using_regex(text)
    assert 'grant@gmail.com' in result['EMAIL']
    assert '658-856-4967' in result['PHONE']
    assert 'Venkata Avinash' in result['PERSON']
    
def test_apply_redaction():
    text = "Contact Avinash at Florida."
    entities = {'PERSON': ['Avinash'], 'ADDRESS': ['Florida']}
    redacted_text = apply_redaction(text, entities, redact_names=True, redact_address=True)
    assert '█' in redacted_text

def test_list_files():
    folder_pattern = "*.py"
    files = list_files(folder_pattern)
    assert isinstance(files, list) and all(f.endswith('.py') for f in files)



def test_get_related_words():
    concept = "call"
    related_words = get_related_words(concept)
    assert isinstance(related_words, list) and 'phone' in related_words



def test_hide_terms_in_sentences():
    text = "The quick brown fox jumps over the lazy dog."
    related_words = ["fox", "dog"]
    redacted_text = hide_terms_in_sentences(text, related_words)
    assert '█' in redacted_text















