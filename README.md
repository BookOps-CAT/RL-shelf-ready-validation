# RL Shelf Ready Record Validator
A validation tool to read and review MARC records provided by vendors.

This tool currently validates EOD to ensure vendors provide consistent order and item data in the records they supply.

## Setup
### Install with pip
1. Create a folder: `$ mkdir rl-validator`
2. Navidate to folder: `$ cd rl-validator`
3. Create a virtual environment and activate it: 
   `$ python -m venv .venv & $ source ./.venv/scripts/activate`
4. Install from Github:
   `$ pip install git+https://github.com/BookOps-CAT/RL-shelf-ready-validation`


### Install with Poetry
1. Clone repository
2. Navigate to project directory in terminal
3. Activate virtual environment in poetry with `$ poetry shell`
4. Install dependencies with `$ poetry install`



## Usage
```
$ validator read
File: temp/test.mrc
```

RL Shelf Ready Record Validator provides a command line interface to view and validate MARC records.
After entering a command, users are prompted to input a file to be read by the tool. This tool can read .mrc files.

### Commands
The following information is also available using `validator --help`

#### Available commands

`$ validator read`

Read and print MARC records one-by-one to terminal

`$ validator read-input`

Convert records and print to terminal. Records are converted to a dict as it would be read by the validator

`$ validator validate-all`

Validates all records in a file and prints output to terminal.

`$ validator validate-brief`

Validates all records in a file and prints summary of errors to terminal.

`$ validator export`

Writes error report to [google sheet](https://docs.google.com/spreadsheets/d/1ZYuhMIE1WiduV98Pdzzw7RwZ08O-sJo7HJihWVgSOhQ/edit?usp=sharing)

#### Combining commands

Commands can also be chained to run together on the same file. 

For example, `$ validator read validate-brief` will read each MARC record and print it to the terminal and when it has finished printing each record it will print a validation summary. Similarly, `$ validator read validate-all` will read a MARC record, print the record to the terminal, validate the MARC record and print the error output to the terminal.

#### Examples
Validate records and export to spreadsheet
```
$ validator validate-all export
File: temp/tests.mrc

Checking all records...

Record #1 (control_no on1381158740) is valid.

Record #2 contains 4 error(s)
     4 missing field/subfield(s): ['980$d', ('item_0', '949$h'), ('item_0', '949$l'), ('item_0', '949$t')]

Record #3 contains 2 error(s)
     2 extra field/subfield(s): ['852$h', ('item_0', '949$a')]
     
Record #4 contains 6 error(s)
     Invalid ReCAP call number: ReCAP 23- 852$h
     3 missing field/subfield(s): ['980$d', ('item_0', '949$i'), ('item_0', '949$h')]
```
Read and validate records
```
$ validator read validate-all
File: temp/tests.mrc

Checking all records...
Printing record #1
=LDR  02060nam a22005295i 4500
=001  on1234567890
=003  OCoLC
=005  20240131000000.0
=008  240131s2024\\\\nyu\\\\\\\\\\\000\0\eng\d
=020  \\$a9781234567890
...
=910  \\$aRL
=949  \1$z8528$aReCAP 24-123456$h43$i33433123456789$p1.00$vVENDOR$lrc2ma$t55
=960  \\$s100$tMAL$u12345apprv
=980  \\$a240131$b100$c000$d000$e100$f10000000$g1

Record #1 (control_no on1381158740) is valid.

```