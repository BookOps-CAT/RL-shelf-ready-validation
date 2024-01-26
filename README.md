# RL Shelf Ready Record Validation
A validation tool to read and review MARC records provided by vendors.

This tool currently validates EOD to ensure vendors provide consistent order and item data in the records they supply.

### Setup
1. Clone repository
2. Navigate to project directory in terminal
3. Activate virtual environment in poetry with `poetry shell`
4. Install dependencies with `poetry install`

### Usage
`validator` provides a command line interface to view and validate MARC records
Users will be prompted to input a file to be read by the tool. `validator` can read .mrc files.



#### Commands
`validator read-marc`
 * Read and print MARC records one-by-one to terminal
`validator read-records`
 * Convert records and print to terminal. Records are converted to a dict in order to be read by the validator
`validator validate-records`
 * Validates records one-by-one. Prints results of validation and, if applicable, a list of errors identified in the record 
`validator validate-all`
 * Validates all records in a file and prints output to terminal.