Name: Venkata Naga Satya Avinash
UFID: 4377-5641

## Project Description

This project involves extracting data from online PDFs provided by the Norman Police Department, reformatting the data, and storing it in an SQLite database. The goal is to build a Python script that can download incident reports, extract specific fields such as incident time, number, location, nature, and ORI, store them in a structured database, and generate summary reports showing the frequency of each incident nature.

The project utilizes Python3, regular expressions, SQL, and Linux command line tools to achieve this. The primary tasks are downloading the incident PDF, extracting data, and inserting it into an SQLite database, followed by generating a report that shows the number of times each nature of incident appears.

## How to Install

1. Install the required dependencies using a package manager like `pipenv`.
2. After setting up the environment, install the dependencies by running the installation commands.
3. In this Project i used package/dependencies are : 
    1. requests
    2. pypdf 
    3. pytest 

## Execution Steps
Step 1: Set up the environment
To install the required dependencies and set up the virtual environment:

Open a terminal and navigate to the project directory.
Run the following command to create the environment and install dependencies:

bash
pipenv install

Step 2: Running the main program
To run the program, you need to provide the URL of the incident report PDF. The script will download the PDF, extract the relevant data, store it in the SQLite database, and generate a summary of incident natures.

bash
pipenv run python project0/main.py --incidents <PDF_URL>
Replace <PDF_URL> with the actual URL of the incident report PDF. For example:

Example
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-02_daily_incident_summary.pdf

Step 3: Running the test cases
The project includes unit tests to ensure the functionality of each component. To run the test cases, use the following command:

bash
pipenv run python -m pytest
This will execute the test cases defined in the test_file.py, verifying the functionality of downloading PDFs, extracting incident data, populating the database, and generating the summary report.


## Expected Output
Upon running the program, you should expect output similar to the following:

911 Call Nature Unknown|4
Abdominal Pains/Problems|4
Alarm|11
Alarm Holdup/Panic|1
Allergies/Envenomations|2
Animal Complaint|3
Animal Dead|2
...
This is a summary showing each incident nature along with the number of occurrences, with each field separated by a pipe (|) and each row terminated by a newline (\n).

## Functions

### `main.py`

- `main()`: 
  - Coordinates the entire process, from downloading the PDF, extracting data, inserting it into the database, and printing a summary report.
  - Parameters: 
    - `url` (string): The URL of the PDF to download and process.
  - Usage: 
    - It takes the PDF URL from the command line, fetches the PDF, extracts data, populates the database, and prints the summary of incident natures.

### `project0.py`

- `fetchincidents(url)`:
  - Downloads the PDF file from the specified URL.
  - Parameters: `url` (string): URL of the PDF file.
  - Returns: Byte stream of the downloaded PDF.
  
- `extractincidents(byte_pdf)`:
  - Extracts the relevant incident details (Date/Time, Incident Number, Location, Nature, and ORI) from the PDF byte stream.
  - Parameters: `byte_pdf`: Byte stream of the PDF.
  - Returns: Five lists containing the respective fields.

- `column_seperator(line)`:
  - Splits a line of text from the PDF into its components: Date/Time, Incident Number, Location, Nature, and ORI.
  - Parameters: `line`: The string line from the PDF.
  - Returns: A tuple containing the extracted fields.



### `database.py`

- `createdb()`:
  - Creates the SQLite database `normanpd.db` and the `incidents` table to store the extracted data.
  - Returns: Database connection object.

- `populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list)`:
  - Populates the `incidents` table in the SQLite database with the extracted data.
  - Parameters: 
    - `conn`: The database connection object.
    - `date_list`, `incident_number_list`, `location_list`, `nature_list`, `ori_list`: Lists of data to insert into the table.

- `status(conn)`:
  - Generates a report showing the number of occurrences of each incident nature, sorted alphabetically and case-sensitively. The output is formatted with each field separated by a pipe character (`|`).
  - Parameters: `conn`: Database connection object.
  - Returns: A string formatted report of incidents and their occurrences.

### `logger.py`

- `setup_logger(log_file)`:
  - Sets up the logging configuration, directing logs to a specified file.
  - Parameters: `log_file`: Path to the log file.
  - Returns: Logger object.

- `log_message(logger, level, message)`:
  - Logs messages with the specified level (info, debug, error).
  - Parameters: 
    - `logger`: The logger object.
    - `level`: Severity level of the log.
    - `message`: Message to log.

### `test_file.py`

This file contains unit tests for the main functions in the project.

- `test_databasecreation()`:
  - Tests that the database is successfully created and connected.
  - Assertions: The database connection is not `None`.

- `test_databaseinsertion()`:
  - Tests that the data is correctly inserted into the `incidents` table.
  - Assertions: The count of records in the `incidents` table is greater than zero.

- `test_download_pdf()`:
  - Tests that the PDF is downloaded from the provided URL.
  - Assertions: The PDF stream is not `None`.

- `test_extract_incidents_from_pdf()`:
  - Tests that incident details are correctly extracted from the PDF.
  - Assertions: All extracted lists contain at least one element.

- `test_column_seperator()`:
  - Tests that lines of text are correctly separated into their respective fields.
  - Assertions: The result matches the expected tuple of extracted fields.

## Database Development

The SQLite database stores the incident data in the `incidents` table with the following fields:
 - DateTime TEXT,
 - IncidentNumber TEXT,
 - Location TEXT,
 - Nature TEXT,
 - IncidentORI TEXT



### Summary Query

To generate a summary of incidents based on their nature, the following SQL query is used:

```sql
SELECT Nature, COUNT(*)
            FROM incidents
            GROUP BY Nature
            ORDER BY Nature ASC
```

## Bugs and Assumptions

1. PDF Structure: The project assumes that the PDF structure will remain consistent. If there are changes, data extraction may fail.
2. Junk Data: The first two rows and the last row of the PDF are assumed to be junk and are ignored.
3. Write Permissions: The script assumes that the `resources` directory has the necessary write permissions to store logs and the database.
4. Field Order: The extracted data is assumed to follow a specific order: Date/Time, Incident Number, Location, Nature, ORI.
