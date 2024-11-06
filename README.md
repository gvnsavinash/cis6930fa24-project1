# Automated Text Redaction System

**Author**: Venkata Naga Satya Avinash , Gudipudi

---

### Overview

This project, built using Python, automates the redaction of sensitive information in text files. It combines regex patterns, SpaCy’s NLP features, and the Pyap library for address to detect and censor specific data types, including personal names, dates, phone numbers, addresses. Users can adjust redaction settings through command-line flags, allowing for flexible data privacy compliance.

---

### Assignment Description

"The assignment aimed to develop a modular, efficient redaction system to handle diverse sensitive data types in large text datasets. It allows user-defined redaction settings and provides detailed statistics on redacted content, ensuring secure and effective data processing."


### Assignment Objective

1. File Selection and Processing: Design the system to accept text files based on a specified glob pattern, allowing single or multiple files (e.g., *.txt) to be selected and processed for redacting sensitive information.
2. Automated Redaction: Develop an automated method to redact text based on both predefined and user-defined criteria, allowing customization according to specific needs.
3. Sensitive Data Redaction: Ensure the system can recognize and redact names, dates, phone numbers, addresses, and specific concepts (e.g., "call" or "house") using synonymous terms in text.
4. Output Generation: Configure the system to save redacted versions of files by appending .censored to the original filename, storing all output files in a specified directory.
5. Statistics and Summary: Allow flexible output options that include statistics summarizing the redacted content to support secure and informed data processing.
6. Accurate Data Detection: Utilize the SpaCy NLP library for identifying and redacting sensitive information, ensuring precise detection of named entities, dates, and any other patterns specified in the project.
7. Batch Processing Capability: Enable batch processing of files with pattern matching for efficient handling of large sets of text files.

### Requirements

To achieve these objectives, the project leverages:
1. **SpaCy** (en_core_web_md model) for Named Entity Recognition (NER).
2. **Regex** for identifying dates, phone numbers, addresses, and email formats.
3. **Pyap** library for detecting U.S. addresses.
4. **NLTK WordNet** to retrieve synonyms and related terms for custom redaction topics.
5. **Logging** to provide traceability and debugging information at each redaction stage.

---

### Installation Guide

1. Install **pipenv** for virtual environment and package management:
   bash :
   pip install pipenv
   

2. Install project dependencies:
   bash :
   pipenv install spacy pytest nltk pyap pycountry us
  

3. Download SpaCy’s `en_core_web_md` model and NLTK’s WordNet:
   bash :
   pipenv run python -m spacy download en_core_web_md
   pipenv run python -m nltk.downloader wordnet
   

4. Install pytest testing framework using the command: 

      pipenv install pytest 


---

### How to run

Run the project with customizable redaction settings using command-line flags:

bash :
pipenv run python redactor.py --input '*.txt' --names --dates --phones --address --concept '<topic>' --output '<file_path>/' --stats stderr


**Example**:
bash :
pipenv run python redactor.py --input '*.txt' --names --dates --phones --address --concept 'call' --output 'files/' --stats stdout

   - This will redact names, dates, phones , address and concept for the given text and save into files directory with a name of sample.censored and sample_stats1.txt 


**Command-line Flags**:
- `--names`, `--dates`, `--phones`, `--address`: Enable redaction for specified entity types.
- `--concept`: Custom term for censoring related sentences.
- `--output`: Directory for saving censored files.
- `--stats`: Specifies where to output redaction statistics (`stderr`, `stdout`, or a file path).

---

**Internal Python Package**
In this project utilizes the us package to directly access U.S. state abbreviations, aiding in the redaction of address information by identifying and redacting state names effectively.

Overview
The us package provides a complete list of U.S. states with their standard abbreviations, such as:

1. "Florida" as "FL"
2. "California" as "CA"
This ensures that state names, when encountered in addresses, are easily identified and redacted without needing additional processing for redacting the address.

### Modules and Function Descriptions

#### 1. **Pattern Matching and Entity Extraction (`pattern_matcher.py`)**

This module defines `extract_using_regex` to perform regex-based entity extraction from text, identifying several predefined entity types.

**`extract_using_regex(text)`**
- **Purpose**:  
   The `extract_using_regex` function extracts specified types of entities from text using regex patterns. The purpose is to identify data points such as names, dates, emails, phone numbers, and addresses, which are commonly sensitive information. This function is essential because it allows customizable and precise identification of sensitive information without requiring machine learning or NLP models. It works by defining a dictionary of patterns for each entity type, then iterating over these patterns and applying `re.findall` to extract matches from the text.

- **Arguments**:
  - `text` (str): The input text from which entities are to be extracted.

- **Returns**:
  - `dict`: Dictionary with entity types (e.g., "PERSON", "EMAIL") as keys and lists of extracted entities as values.

- **Details**:
**Regex Patterns**
1. PERSON
      Identify Names 
      Examples:
      "Emily"
      "Smith"
      "David Johnson"
2. EMAIL
    Matches standard email formats, allowing for the extraction of names. For instance, in Emily@gmail.com, "Emily" is recognized as the name.

    Examples:
    "mary_smith@yahoo.com"
    "alice.jones@company.co.uk"
    "user123@domain.org"
    "contact.me@service.com"
    "info@business.site"
    "test.email+filter@gmail.com"
    "firstname.lastname@company.com"
    "my.email@subdomain.domain.com"
    "customer.service@helpdesk.net"
3. PHONE
Matches phone numbers in both common and international formats, accounting for country codes, separators, and area codes.

    Examples:
    "(555) 123-4567"
    "555-987-6543"
    "+1 800 555 0199"
    "1-800-555-0199"
    "555.555.1212"

4. ADDRESS
Recognizes Address in various Format 

Examples:
" New York "
"789 Park Blvd, Room 101, Houston"

5. DATE
Supports a variety of date formats, including long/short month names and numeric formats.

Examples:
    "01/15/2022"
    "2022-03-25"
    "11-30-2024"
    "March 25, 2022"
    "25th March 2022"
    "Fri, 25 Mar 2022"
    "2022/03/25"
    "25.03.22"
    "March 2022"
    "03-25-22"


Functionality
This system relies on predefined regex patterns to accurately identify each entity type, ensuring that only explicitly defined patterns are matched. This approach minimizes false positives and guarantees precise data extraction, facilitating secure processing of sensitive information.

- **Example Usage**:
  ```python
  text = "Emily was born on October 31, 2024. His email is Emily@example.com."
  extract_using_regex(text)
  ```
- **Logging**: The function logs extraction results for each entity type at the debug level, helping trace its performance during execution.

  This log file records debugging information throughout the redaction process. Key details include (This will saved on docs/codelogger.log):

    1. File Listing: Logs the files retrieved based on specified patterns (e.g., text_files/*.txt).
    2. Entity Extraction: Captures the results of regex-based entity extraction, showing entities identified as PERSON, EMAIL, PHONE, ADDRESS, and DATE. The log notes each type, along with any matched patterns (e.g., phone numbers, addresses).
    3. Extraction Stages: The file logs various processing stages, such as "Regex Extraction" and "SpaCy NER Extraction," including the lists of entities identified at each stage.
    4. Output Results: Provides statistics on the redacted information, summarizing counts of names, dates, phone numbers, and addresses identified.
    5. This log helps trace each step of the tool’s execution, providing insights into the regex matches, entity extraction outcomes, and overall redaction statistics, making it valuable for debugging and verifying the redaction process

#### 2. **Helper Functions for Redaction (`helper.py`)**

This module includes several helper functions to perform redaction and manage file operations. It also includes internal functions for retrieving related terms and censoring sentences based on a list of keywords. Here i used RedactorClass where it consists of global variables which it helps for other functions to track and count the values , details of all functions (hide_terms_in_sentences , apply_redaction ) inside of class as follows : 

**`apply_redaction(text, entities, redact_names=False, redact_dates=False, redact_phones=False, redact_address=False, redact_topics=[])`**
- **Purpose**:  
   `apply_redaction` censors sensitive entities in the input text by replacing them with block characters (`█`). It uses the provided flags to determine which entities to redact, then iterates over the entities in the text, matching and replacing occurrences. This function provides flexibility in what to redact based on command-line arguments. After entity redaction, if any additional topics are specified in `redact_topics`, the function calls `hide_terms_in_sentences` to censor entire sentences containing these terms.

- **Arguments**:
  - `text` (str): Input text to be redacted.
  - `entities` (dict): Dictionary where each key is an entity type (e.g., "PERSON") and each value is a list of entities.
  - `redact_names`, `redact_dates`, `redact_phones`, `redact_address` (bool): Flags to indicate which entity types to redact.
  - `redact_topics` (list): List of additional terms or topics to redact in full sentences.

- **Returns**:
  - `str`: Text with redacted entities and topics replaced by `█` characters.

- **Internal Mechanics**:
   - `apply_redaction` begins by setting up a dictionary that maps each entity type to its redaction flag (e.g., `redact_names` for `PERSON`).
   - For each entity type that has a corresponding flag enabled, it replaces each occurrence with a redacted version.
   - After entity-level redaction, if `redact_topics` is specified, it calls `hide_terms_in_sentences` to handle sentence-level redaction based on the specified topics.

- **Example Usage**:
  ```python
  apply_redaction("Contact Emily at 555-456-7890.", {"PERSON": ["Emily"], "PHONE": ["555-456-7890"]}, redact_names=True, redact_phones=True)
  ```

**`hide_terms_in_sentences(text, related_words)`**
- **Purpose**:  
   This function redacts entire sentences containing any word in the `related_words` list. It first splits the text into sentences, then checks each sentence for matches. If a match is found, the sentence is replaced with a redacted block. This function is particularly useful for concept-based redaction, where specific words in a sentence warrant full censorship.

- **Arguments**:
  - `text` (str): Input text.
  - `related_words` (list): List of words to search for within sentences.

- **Returns**:
  - `str`: Text with redacted sentences.

**`list_files(folder_pattern)`**
- **Purpose**:  
   Lists files in the directory that match a specified pattern (e.g., “*.txt”). This is useful for batch processing of files, allowing the tool to process single/multiple files in one run. The function uses the glob module, making it compatible with Unix-style wildcards for flexible file selection.

- **Arguments**:
  - `folder_pattern` (str): Pattern for matching files, such as “*.txt” to match all text files.

- **Returns**:
  - `list`: List of file paths that match the specified pattern.

**`get_related_words(concept)`**
- **Purpose**:  
   Retrieves a list of related terms for a specified concept using WordNet. This function expands redaction coverage by including synonyms, hypernyms (broader terms), and hyponyms (more specific terms) for the provided concept. This additional coverage ensures that the redaction process accounts for a broader scope of related words, enhancing data security.

- **Arguments**:
  - `concept` (str): Concept or term for which related terms should be identified.

- **Returns**:
  - `list`: List of related terms for redaction.

- **Internal Mechanics**:
  - `get_related_words` uses the `wordnet` module to find synonyms, hypernyms, and hyponyms. Each term is processed to remove WordNet suffixes (e.g., “.n.01”), ensuring the terms appear in a natural language format.



#### 3. **Main Redaction Functionality (`redactor.py`)**

The main script combines all helper functions, regex, and NLP

 processing into a comprehensive redaction workflow.

**`find_addresses_with_pyap(text)`**
- **Purpose**:  
   Finds U.S. addresses within the input text using the Pyap library. This function supplements the regex-based address extraction by leveraging Pyap’s built-in patterns for U.S. address formats, enhancing accuracy in redacting geographic data.

- **Arguments**:
  - `text` (str): Input text to search for addresses.

- **Returns**:
  - `list`: List of addresses found in the text.

**`print_debug_info(stage, names=None, dates=None, phones=None, addresses=None)`**
- **Purpose**:  
   Logs detailed debug information at various stages of processing. This function helps trace each extraction and redaction phase, outputting entities identified at each stage (e.g., after regex extraction or SpaCy processing). The purpose is to aid debugging and verification during development.

- **Arguments**:
  - `stage` (str): Current stage of processing.
  - `names`, `dates`, `phones`, `addresses` (list, optional): Lists of extracted entities for logging.

**`format_entity_stats(file, args, names, dates, phones, addresses)`**
- **Purpose**:  
   Formats statistics on redacted entities for output. The function constructs a summary of all redacted entities (e.g., names, dates, phones etc ) for each processed file. The purpose is to provide a concise report of what was redacted in each file, supporting data governance and tracking.

- **Arguments**:
  - `file` (str): The name of the processed file.
  - `args` (Namespace): Command-line arguments controlling which entities to include.
  - `names`, `dates`, `phones`, `addresses` (list): Lists of entities found.
  - redacted_words_count (int): The count of redacted words.
  - redacted_sentences_count (int): The count of redacted sentences.

- **Returns**:
  - `str`: Formatted string with redaction statistics.

## The stdout/stderr/file format
The stats structure will be outputted in the following format after running the file using the above command.

*Format:*

                File: <file.txt>, 
                Names: 0, 
                Dates: 0, 
                Phones: 0, 
                Addresses: 0, 
                Concept redacted_words_count : 0,
                Concept redacted_sentences_count : 0
  {'Names': [], 'Dates': [], 'Phones': [], 'Addresses': [], 'Set_Concept_Words': {}}

*Sample Output:*

                File: sample.txt, 
                Names: 2, 
                Dates: 1, 
                Phones: 1, 
                Addresses: 2, 
                Concept redacted_words_count : 4,
                Concept redacted_sentences_count : 4

  Detailed information on identified entities in the file:
{'Names': ['Alice', 'Sophia'], 'Dates': ['4/9/2025', '22/2/22'], 'Phones': ['+1 (305) 555-1234', '+1 (420) 794-0958'], 'Addresses': ['123 Maple St', 'Maple St', '987 Cedar St'], 'Set_Concept_Words': {'phone', 'see', 'Call', 'meet'}}


**`redact_sensitive_info(text_input, args, topics=None)`**
- **Purpose**:  
   The primary redaction function, `redact_sensitive_info`, manages the entire process. It reads the input text, extracts entities using regex and SpaCy, combines results, and then applies redactions based on the flags specified in `args`. This function serves as the backbone of the redaction system, orchestrating regex and NLP-based extraction and coordinating calls to other functions (like `apply_redaction` and `find_addresses_with_pyap` (which i already explaned above) ) for comprehensive redaction.

- **Arguments**:
  - `text_input` (str): Path to the file or the text content itself.
  - `args` (Namespace): Flags for different redaction types.
  - `topics` (list, optional): Custom topics for concept-based redaction.

- **Returns**:
  - `tuple`: Contains redacted text, and lists of identified names, dates, phones, and addresses.

**`main(args)`**
- **Purpose**:  
   The main function orchestrates the entire redaction workflow. It parses command-line arguments, processes files, applies redactions, and saves outputs. Additionally, it generates redaction statistics, saving them in the output directory. This function is the entry point when running `redactor.py` as a standalone script.

- **Arguments**:
  - `args` (Namespace): Command-line arguments controlling input, output, and redaction options.

---

**Stats file** 

This script offers three modes for outputting statistics and detailed information about the redacted entities:

**Standard Error (stderr):** Directs the output to the standard error stream, useful for error logging and diagnostics.
**Standard Output (stdout):** Directs the output to the standard output stream, ideal for real-time monitoring in a console.
**File Output:** Directs the output to a specified file, creating the file if it does not exist, and appending to it if it does.

**Handling Multiple Files**
When processing multiple files, the script appends the statistics and details for each input file into the designated one output file specified by the user for stats. This allows for consolidated logging of all processed information in one place, making it easier to review and analyze data across multiple documents.


## Test File

**test_extract_using_regex()**

Purpose:
The test_extract_using_regex function validates the extract_using_regex function by ensuring it accurately extracts information like names, emails, and phone numbers using regex. This test is essential to verify the function’s ability to correctly identify sensitive entities within a given text based on pattern matching.
Arguments:
None; the function internally defines the test text and expected values.
Assertions:
Checks that extract_using_regex outputs a dictionary where:
The EMAIL key includes 'grant@gmail.com'.
The PHONE key includes '658-856-4967'.
The PERSON key includes 'Venkata Avinash'.


**test_apply_redaction()**

Purpose:
This function tests the apply_redaction function to ensure it properly redacts entities in a given text. The goal is to confirm that when apply_redaction is instructed to redact names and addresses, the output contains redaction characters (█) in place of the specified entities, demonstrating the function’s effectiveness in hiding sensitive information.
Arguments:
None; the function internally defines the test text, entities to redact, and flags to indicate what to redact.
Assertions:
Verifies that the output contains the redaction character (█) where "Avinash" (name) and "Florida" (address) are expected to be redacted.


**test_get_related_words()**

Purpose:
The test_get_related_words function checks the functionality of get_related_words by verifying that it returns appropriate related terms for a given concept. This test is crucial for confirming that the function can identify relevant synonyms or terms, ensuring broader coverage in concept-based redaction.
Arguments:
None; the function internally defines the concept to be tested.
Assertions:
Asserts that the result is a list.
Confirms that the word "phone" is present in the list of related words for the concept "call."

**test_hide_terms_in_sentences()**

Purpose:
This function validates the hide_terms_in_sentences function to ensure that it correctly redacts specified terms within sentences. By checking that the terms "fox" and "dog" are replaced with redaction characters (█), the test confirms that the function can accurately hide terms that match specific criteria, essential for topic-based redaction.
Arguments:
None; the function defines the input text and terms to be redacted internally.
Assertions:
Checks that the output contains the redaction character (█) .

---

## Bugs and Assumptions

1. Regex and NLP Limitations
  1. Based on the project’s design, the entity extraction depends heavily on regex patterns and SpaCy’s NLP model. While these methods are effective for common formats, they might miss entities that don’t follow standard structures, particularly with names, addresses, and phone numbers.
  2. The address regex pattern is built around specific assumptions like full street names and postal codes, so addresses missing these elements or with abbreviations may not be properly redacted.
  3. The SpaCy model is optimized for English, so redaction may be less accurate for non-English texts.

2. File Format and Input Assumptions
  1. This tool is most effective with well-structured text that adheres to standard rules for punctuation, spacing, and capitalization. If the input text has inconsistent or non-standard formatting, the redaction results might not be as accurate.
  2. It’s designed to handle plain text files and doesn’t account for complex document formats like PDFs with embedded images or structured formats like HTML or JSON. This limits its effectiveness when handling highly formatted or data-rich text structures.

3. Dependency and Encoding Constraints
  1. The project uses several external libraries (SpaCy, Pyap, NLTK), each with unique installation requirements. An initial internet connection is needed to download WordNet data for NLTK, which may affect usage in offline environments.
  2. TF-8 encoding is assumed for all input files; files with different encodings, particularly those containing special characters, might not process correctly. Also, the use of Unix-style patterns for batch processing can create compatibility issues on some systems, particularly Windows.

4. I didn’t have the opportunity to use Snorkel’s LFApplier or LabelModel in this project. However, I utilized Snorkel’s labeling_function decorator to enhance my regex_match function. By applying this decorator, the function can now ABSTAIN when it doesn’t find relevant matches, instead of assigning a random label. This ensures higher accuracy by avoiding uncertain or arbitrary labels when the function lacks sufficient information.

5. Security and Privacy Considerations
  1. Since redacted files are stored in the output directory, any incomplete redaction could expose sensitive data. Therefore, it’s crucial to restrict access to this directory.
  2. The tool assumes a text-based input structure, which means it may struggle with heavily formatted or nested data types like JSON or XML. This assumption could limit its utility when working with more complex data formats.

6. I didn’t have the opportunity to use Snorkel’s LFApplier or LabelModel in this project. However, I utilized Snorkel’s labeling_function decorator to enhance my regex_match function. By applying this decorator, the function can now ABSTAIN when it doesn’t find relevant matches, instead of assigning a random label. This ensures higher accuracy by avoiding uncertain or arbitrary labels when the function lacks sufficient information.

