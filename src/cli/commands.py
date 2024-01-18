import click
from src.validate.models import Record
from src.validate.errors import (
    get_error_count,
    format_error_messages,
)
from src.validate.translate import (
    read_marc_to_dict,
    read_marc_records,
    convert_to_input,
)
from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme

theme = Theme(
    {
        "error_count": "bold red",
        "record_number": "bold cyan",
        "control_no": "bold magenta",
    }
)
console = Console(tab_size=5, theme=theme)


@click.group()
def cli():
    pass


@cli.command("read-records-as-marc")
@click.option("-f", "--file", prompt=True)
def read_records_as_marc(file):
    records = read_marc_records(file)
    n = 0
    while True:
        for record in records:
            n += 1
            console.print(f"Printing record [record_number]#{n}[/record_number]")
            console.print(record)
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("read-records")
@click.option("-f", "--file", prompt=True)
def read_records(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = convert_to_input(record)
            console.print(f"Printing record [record_number]#{n}[/record_number]")
            console.print(converted_record)
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("validate-records")
@click.option("-f", "--file", prompt=True)
def validate_records(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = convert_to_input(record)
            try:
                Record(**converted_record)
                console.print(f"Record #{n} is valid.")
            except ValidationError as e:
                formatted_errors = format_error_messages(e)
                error_count = get_error_count(e)
                console.print(
                    f"Record [record_number]#{n}[/record_number] contains [error_count]{error_count} error(s)[/error_count]"
                )
                for error in formatted_errors:
                    console.print(f"\t{error[0]}: {error[1]}")
            click.pause(info="Press any key to read and validate next record\n")
        console.print("No more records")
        break


@cli.command("validate-all")
@click.option("-f", "--file", prompt=True)
def validate_all(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        # output_list = []
        console.print("\n\nChecking all records...")
        console.print("Printing results...\n\n")
        for record in records:
            n += 1
            converted_record = convert_to_input(record)
            control_number = converted_record["control_number"]
            console.print(
                f"\n\n[record_number]Record #{n}[/record_number] (control_no [control_no]{control_number}[/control_no])"
            )
            try:
                Record(**converted_record)
                console.print(f"Validated successfully!")
            except ValidationError as e:
                formatted_errors = format_error_messages(e)
                error_count = get_error_count(e)
                console.print(
                    f"Record contains [error_count]{error_count} error(s)[/error_count]:"
                )
                for error in formatted_errors:
                    console.print(f"\t{error[0]}: {error[1]}")
        console.print("Finished checking records.")
        break
