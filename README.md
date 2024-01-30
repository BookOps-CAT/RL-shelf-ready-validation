# RL Shelf Ready Record Validation
A validation tool to read and review MARC records provided by vendors.

This tool currently validates EOD to ensure vendors provide consistent order and item data in the records they supply.

### Setup
#### Install with pip
1. Create a folder: `$ mkdir rl-validator`
2. Navidate to folder: `$ cd rl-validator`
3. Create a virtual environment and activate it: 
   `$ python -m venv .venv & $ source ./.venv/scripts/activate`
4. Install from Github:
   `$ pip install git+https://github.com/BookOps-CAT/RL-shelf-ready-validation`


#### Install with Poetry
1. Clone repository
2. Navigate to project directory in terminal
3. Activate virtual environment in poetry with `poetry shell`
4. Install dependencies with `poetry install`



### Usage
`validator` provides a command line interface to view and validate MARC records
Users will be prompted to input a file to be read by the tool. `validator` can read .mrc files.


#### Commands
The following information is also available using `validator --help`

`validator read`
 * Read and print MARC records one-by-one to terminal
`validator read-input`
 * Convert records and print to terminal. Records are converted to a dict in order to be read by the validator
`validator validate-all`
 * Validates all records in a file and prints output to terminal.
`validator validate-brief`
 * Validates all records in a file and prints summary of errors to terminal.
`validator validate-record`
 * Validates records one-by-one. Prints results of validation and, if applicable, a list of errors identified in the record 
