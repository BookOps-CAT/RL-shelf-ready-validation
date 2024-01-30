import click
from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme
from functools import update_wrapper
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


@click.group(chain=True)
@click.option(
    "--file",
    "file",
    prompt=True,
    help="Provide the filename for the file you would like to open.",
)
def cli(file):
    """
    Read and validate MARC records

    """
    pass


@cli.result_callback()
def process_commands(processors, file):
    # Start with MARC file.
    reader = read_marc_records(file)
    # Pipe it through all processors.
    for processor in processors:
        reader = processor(reader)
    for _ in reader:
        pass


def processor(f):
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


@cli.command("read")
@processor
def read_marc(reader):
    """
    Print MARC records in terminal
    """
    n = 0
    while True:
        for record in reader:
            n += 1
            console.print(f"Printing record [marc_record]#{n}[/]")
            console.print(record)
            yield record
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("read-input")
@processor
def read_input(reader):
    """
    Convert MARC record to input, print to terminal
    """
    n = 0
    while True:
        for record in reader:
            n += 1
            converted_record = get_record_input(record)
            console.print(f"Printing record [marc_record]#{n}[/]")
            console.print(converted_record)
            yield converted_record
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("validate-all")
@processor
def validate_all(reader):
    """
    Validate all records in file, print all errors
    """
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
                    output = f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    console.print(output)
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["input"] == error["loc"]:
                            output = f"\t{error['msg']}: {error['loc']}"
                            console.print(output)

                        else:
                            output = (
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )
                            console.print(output)

            else:
                try:
                    OtherMaterialRecord(**record_input)
                    output = f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/]) is valid."
                    console.print(output)
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = e.error_count()
                    console.print(
                        f"\n\nRecord [marc_record]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        if error["input"] == error["loc"]:
                            output = f"\t{error['msg']}: {error['loc']}"
                            console.print(output)

                        else:
                            output = (
                                f"\t{error['msg']}: {error['input']} {error['loc']}"
                            )
                            console.print(output)
        yield output
        break


@cli.command("validate-brief")
@processor
def validate_summary(reader):
    """
    Validate all records in file, print summary of errors
    """
    total_records = 0
    invalid_records = 0
    valid_records = 0
    errored_records = []
    while True:
        for record in reader:
            total_records += 1
            control_number = record["001"].data
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            if record_type == "monograph_record":
                try:
                    MonographRecord(**record_input)
                    valid_records += 1
                except ValidationError as e:
                    invalid_records += 1
                    error_count = e.error_count()
                    error_output = (control_number, error_count)
                    errored_records.append(error_output)
            else:
                try:
                    OtherMaterialRecord(**record_input)
                    valid_records += 1
                except ValidationError as e:
                    invalid_records += 1
                    error_count = e.error_count()
                    error_output = (control_number, error_count)
                    errored_records.append(error_output)
        if invalid_records > 0:
            output = f"\nFile contains {total_records} record(s): {valid_records} valid record(s) and [error_count]{invalid_records} invalid record(s)[/]. \n\n[error_count]Invalid record list and error count:[/] \n{errored_records} \n\nFor more detailed error information run `validator validate-all`"
        else:
            output = f"\nFile contains {total_records} valid record(s)"
        yield output
        console.print(output)
        break


def main():
    cli()
