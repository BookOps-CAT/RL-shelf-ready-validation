import click
from click import Context
import pandas as pd
from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme
from functools import update_wrapper
from shelf_ready_validator.models import MonographRecord, OtherMaterialRecord
from shelf_ready_validator.errors import format_errors, format_error_summary
from shelf_ready_validator.translate import (
    get_material_type,
    get_record_input, read_marc_records
)

theme = Theme(
    {
        "error": "bold red",
        "record": "bold cyan",
        "control_no": "bold magenta",
    }
)
console = Console(tab_size=5, theme=theme)


@click.group(chain=True)
@click.option(
    "--file",
    "file",
    prompt=True,
    help="The MARC file you would like to open.",
)
def cli(file):
    """
    Read and validate MARC records

    """
    pass


@cli.result_callback()
def process_commands(processors, file):
    """
    Creates iterator for all records in a MARC file
    Runs record through each function that is called by the command input
    This function will return a TypeError if a command is called that does not return a value
    """
    reader = read_marc_records(file)

    for processor in processors:
        reader = processor(reader)
    for record in reader:
        pass


def processor(f):
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


@cli.command("read", short_help="print MARC records")
@processor
def read_marc(reader):
    """
    Prints MARC records from file one-by-one
    """
    n = 0
    while True:
        for record in reader:
            n += 1
            console.print(f"Printing record [record]#{n}[/]")
            console.print(record)
            yield record
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("read-input", short_help="print records as dict")
@processor
def read_input(reader):
    """
    Converts MARC record to dict input that is used by validator
    Prints dict to terminal
    """
    n = 0
    while True:
        for record in reader:
            n += 1
            converted_record = get_record_input(record)
            console.print(f"Printing record [record]#{n}[/]")
            console.print(converted_record)
            yield converted_record
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("validate-all", short_help="validate all records")
@processor
def validate_all(reader):
    """
    Loops through file of MARC records and validate each record
    Prints errors for each record to terminal
    Creates a dict output of errors for each record and adds the output to a list
    Returns dict output to use with export command
    """
    n = 0
    output = []
    while True:
        console.print("\nChecking all records...")
        for record in reader:
            n += 1
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            out_report = {
                "vendor_code": record_input["bib_vendor_code"],
                "record_number": n,
                "control_number": record["001"].data,
            }
            if record_type == "monograph_record":
                try:
                    MonographRecord(**record_input)
                    out_report["valid"] = True
                    console.print(f"\n[record]Record #{n}[/] (control_no [control_no]{record["001"].data}[/]) is valid.")
                except ValidationError as e:
                    out_report["valid"] = False
                    out_report["error_count"] = str(e.error_count())
                    error_summary = format_error_summary(e)
                    out_report.update(error_summary)
                    console.print(
                        f"\nRecord [record]#{n}[/] contains [error]{e.error_count()} error(s)[/]"
                    )
                    formatted_errors = format_errors(e)
                    for error in formatted_errors:
                        if error["type"] == "missing":
                            console.print(f"\t{error["count"]} {error['msg']}: {error['loc']}")
                        elif error["type"] == "extra_forbidden":
                            console.print(f"\t{error["count"]} {error['msg']}: {error['loc']}")
                        else:
                            console.print(f"\t{error['msg']}: {error['input']} {error['loc']}")
                output.append(out_report)
            else:
                try:
                    OtherMaterialRecord(**record_input)
                    out_report["valid"] = True
                    console.print(f"\n[record]Record #{n}[/] (control_no [control_no]{record["001"].data}[/]) is valid.")
                except ValidationError as e:
                    out_report["valid"] = False
                    out_report["error_count"] = e.error_count()
                    error_summary = format_error_summary(e)
                    out_report.update(error_summary)
                    console.print(
                        f"\nRecord [record]#{n}[/] contains [error]{e.error_count()} error(s)[/]"
                    )
                    formatted_errors = format_errors(e)
                    for error in formatted_errors:
                        if error["type"] == "missing":
                            console.print(f"\t{error["count"]} {error['msg']}: {error['loc']}")
                        elif error["type"] == "extra_forbidden":
                            console.print(f"\t{error["count"]} {error['msg']}: {error['loc']}")
                        else:
                            console.print(f"\t{error['msg']}: {error['input']} {error['loc']}")
                output.append(out_report)
        yield output
        break


@cli.command("validate-brief", short_help="get validation summary")
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
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            control_number = record["001"].data
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
            output = f"\nFile contains {total_records} record(s): {valid_records} valid record(s) and [error]{invalid_records} invalid record(s)[/]. \n\n[error]Invalid record list and error count:[/] \n{errored_records} \n\nFor more detailed error information run `validator validate-all`"
        else:
            output = f"\nFile contains {total_records} valid record(s)"
        console.print(output)
        yield output
        break


@cli.command("export", short_help="export validation report")
@processor
def export_error_report(output):
    """
    Writes error report from validate-all command to file
    """
    for out in output:
        output_df = pd.DataFrame(out)
        console.print(output_df)
        yield output_df


def main():
    cli()
