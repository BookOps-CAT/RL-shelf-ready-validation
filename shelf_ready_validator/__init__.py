import click
import pandas as pd
from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme
from functools import update_wrapper
from shelf_ready_validator.models import MonographRecord, OtherMaterialRecord
from shelf_ready_validator.errors import format_errors
from shelf_ready_validator.translate import (
    get_material_type,
    get_record_input,
    read_marc_records,
)
from shelf_ready_validator.sheet import write_sheet
from datetime import datetime
import io

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
@click.pass_context
def cli(ctx, file):
    """
    Read and validate MARC records

    """
    file_input = io.BytesIO(file.encode("utf-8"))
    ctx.obj = io.TextIOWrapper(file_input, encoding="utf-8").read()
    pass


@cli.result_callback()
def process_commands(processors, file):
    """
    Creates iterator for all records in a MARC file.
    Runs record through each function that is called by the command input.
    Return a TypeError if a command is called that does not return a value.
    """
    reader = read_marc_records(file)

    for processor in processors:
        reader = processor(reader)
    for record in reader:
        pass


def processor(f):
    """
    A decorator for all functions that process MARC data or validation data.
    """

    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


@cli.command("read", short_help="read MARC records")
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


@cli.command("read-input", short_help="print records as dictionary")
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
                    console.print(
                        f"\n[record]Record #{n}[/] (control_no [control_no]{record['001'].data}[/]) is valid."
                    )
                except ValidationError as e:
                    out_report["valid"] = False
                    error_summary = format_errors(e)
                    console.print(
                        f"\nRecord [record]#{n}[/] contains [error]{error_summary['error_count']} error(s)[/]"
                    )
                    if error_summary["missing_field_count"] > 0:
                        console.print(
                            f"\t{error_summary['missing_field_count']} missing field/subfield(s): {error_summary['missing_fields']}"
                        )
                    if error_summary["extra_field_count"] > 0:
                        console.print(
                            f"\t{error_summary['extra_field_count']} extra field/subfield(s): {error_summary['extra_fields']}"
                        )
                    for error in error_summary["errors"]:
                        console.print(
                            f"\t{error['msg']}: {error['input']} {error['loc']}"
                        )
                    del error_summary["errors"]
                    out_report.update(error_summary)
                output.append(out_report)
            else:
                try:
                    OtherMaterialRecord(**record_input)
                    out_report["valid"] = True
                    console.print(
                        f"\n[record]Record #{n}[/] (control_no [control_no]{record['001'].data}[/]) is valid."
                    )
                except ValidationError as e:
                    out_report["valid"] = False
                    error_summary = format_errors(e)
                    console.print(
                        f"\nRecord [record]#{n}[/] contains [error]{error_summary['error_count']} error(s)[/]"
                    )
                    if error_summary["missing_field_count"] > 0:
                        console.print(
                            f"\t{error_summary['missing_field_count']} missing field/subfield(s): {error_summary['missing_fields']}"
                        )
                    if error_summary["extra_field_count"] > 0:
                        console.print(
                            f"\t{error_summary['extra_field_count']} extra field/subfield(s): {error_summary['extra_fields']}"
                        )
                    for error in error_summary["errors"]:
                        console.print(
                            f"\t{error['msg']}: {error['input']} {error['loc']}"
                        )
                    del error_summary["errors"]
                    out_report.update(error_summary)
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


@cli.command("validate-raw", short_help="get raw validation errors")
@processor
def validate_raw(reader):
    """
    Returns raw validation error output
    """
    errored_records = []
    n = 0
    while True:
        for record in reader:
            n += 1
            record_input = get_record_input(record)
            record_type = get_material_type(record)
            control_number = record["001"].data
            if record_type == "monograph_record":
                try:
                    MonographRecord(**record_input)
                    console.print(
                        f"Record # {n} (control no {control_number}) validates"
                    )
                except ValidationError as e:
                    console.print(
                        f"Record #{n} (control no {control_number}) has errors"
                    )
                    console.print(e.errors())
                    errored_records.append(e.errors())
            else:
                try:
                    OtherMaterialRecord(**record_input)
                    console.print(
                        f"Record # {n} (control no {control_number} validates"
                    )
                except ValidationError as e:
                    console.print(
                        f"Record #{n} (control no {control_number}) has errors"
                    )
                    console.print(e.errors())
                    errored_records.append(e.errors())
        yield errored_records
        break


@cli.command("export", short_help="export validation report")
@processor
@click.pass_obj
def export_error_report(filename, output):
    """
    Writes error report from validate-all command to file
    """
    for out in output:
        output_df = pd.DataFrame(out, dtype="string")
        output_df = output_df.fillna("None")
        file = filename.split("/")[-1]
        output_df.insert(loc=0, column="filename", value=file)
        output_df.insert(
            loc=0,
            column="validation-date",
            value=datetime.today().strftime("%Y-%m-%d %I:%M:%S"),
        )
        rows = output_df.values.tolist()
        write_sheet(
            "1ZYuhMIE1WiduV98Pdzzw7RwZ08O-sJo7HJihWVgSOhQ",
            "RecordOutput!A1:M10000",
            "USER_ENTERED",
            "INSERT_ROWS",
            rows,
        )
        yield output_df


def main():
    cli()
