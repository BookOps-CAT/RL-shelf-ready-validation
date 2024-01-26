import click
from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme

from shelf_ready_validator.models import MonographRecord, OtherMaterialRecord
from shelf_ready_validator.errors import format_error_messages
from shelf_ready_validator.translate import (
    read_marc_records,
    get_material_type,
    get_record_input,
)

theme = Theme(
    {
        "error_count": "bold red",
        "marc_record": "bold cyan",
        "control_no": "bold magenta",
    }
)
console = Console(tab_size=5, theme=theme)


@click.group()
def cli():
    """
    A program that reads and validates MARC records from vendors
    """
    pass


@cli.command("read-marc")
@click.option(
    "-f",
    "--file",
    prompt="File",
    help="Path to file you would like to read or validate.",
)
def read_marc(file):
    """
    Read MARC records and print in terminal
    """
    records = read_marc_records(file)
    n = 0
    while True:
        for record in records:
            n += 1
            console.print(f"Printing record [marc_record]#{n}[/]")
            console.print(record)
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("read-records")
@click.option(
    "-f",
    "--file",
    prompt="File",
    help="Path to file you would like to read or validate.",
)
def read_records(file):
    """
    Print converted MARC in terminal
    """
    records = read_marc_records(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = get_record_input(record)
            console.print(f"Printing record [marc_record]#{n}[/]")
            console.print(converted_record)
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("validate-records")
@click.option(
    "-f",
    "--file",
    prompt="File",
    help="Path to file you would like to read or validate.",
)
def validate_records(file):
    """
    Read and validate records one-by-one
    """
    reader = read_marc_records(file)
    n = 0
    while True:
        for record in reader:
            n += 1
            control_number = record["001"].data
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            if record_type == "monograph_record":
                try:
                    MonographRecord(**record_input)
                    console.print(
                        f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    )
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["input"] == error["loc"]:
                            console.print(f"\t{error['msg']}: {error['loc']}")

                        else:
                            console.print(
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )

            else:
                try:
                    OtherMaterialRecord(**record_input)
                    console.print(
                        f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    )
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["input"] == error["loc"]:
                            console.print(f"\t{error['msg']}: {error['loc']}")

                        else:
                            console.print(
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )
            click.pause(info="Press any key to read and validate next record\n")
        console.print("No more records")
        break


@cli.command("validate-all")
@click.option(
    "-f",
    "--file",
    prompt="File",
    help="Path to file you would like to read or validate.",
)
def validate_all(file):
    """
    Validate all records in a file
    """
    reader = read_marc_records(file)
    n = 0
    while True:
        console.print("\n\nChecking all records...")
        console.print("Printing results...\n\n")
        for record in reader:
            n += 1
            control_number = record["001"].data
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            if record_type == "monograph_record":
                try:
                    MonographRecord(**record_input)
                    console.print(
                        f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    )
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["input"] == error["loc"]:
                            console.print(f"\t{error['msg']}: {error['loc']}")

                        else:
                            console.print(
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )

            else:
                try:
                    OtherMaterialRecord(**record_input)
                    console.print(
                        f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    )
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["type"] == "union_tag_invalid":
                            console.print(error)
                            break
                        if error["input"] == error["loc"]:
                            console.print(f"\t{error['msg']}: {error['loc']}")

                        else:
                            console.print(
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )
        console.print("Finished checking records.")
        break


def main():
    cli()
