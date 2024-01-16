import click
from pymarc import MARCReader
from src.validate.models import Record
from src.validate.translate import read_marc_records
from src.validate.errors import convert_error_messages
from pydantic import ValidationError

"""
what I want this to do:
user types cli command and gets list of available commands
 - read records
    - returns count of records and maybe titles or 001
 - validate records
    - first returns count of records and titles or 001
    - asks if records should be validated
    - then asks if errors should be printed in cli or writen to file


 ... future options:
 - edit records
 - 

cli needs to be able to take file input and specify file output

"""


@click.group()
@click.option("-f", "--file")
@click.option("-r", "--read", "read")
@click.option("-rv", "--read_validate", "read_validate")
def cli():
    pass


@click.command()
def intro():
    click.echo("MARC Record Validator")


@click.command()
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def read_records(input):
    record = read_marc_records(input)
    return record


@click.command
# option to
def validate_records(input):
    try:
        Record(**input)
    except ValidationError as e:
        formatted_errors = convert_error_messages(e)
        return formatted_errors


cli.add_command(intro)
cli.add_command(r_w_records)

if __name__ == "__main__":
    cli()
