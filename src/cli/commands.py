import click
from src.validate.models_v2 import MonographRecord, OtherMaterialRecord
from src.validate.errors import (
    get_error_count,
    format_error_messages,
)
from src.validate.translate import (
    read_marc_records,
    get_material_type,
    get_record_input,
)

from pydantic import ValidationError
from rich.console import Console
from rich.theme import Theme

theme = Theme(
    {
        "error_count": "bold red",
        "record_number": "bold cyan",
        "control_no": "bold magenta",
        "marc_field": "bold cyan",
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
def read_records_as_input(file):
    records = read_marc_records(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = get_record_input(record)
            console.print(f"Printing record [record_number]#{n}[/record_number]")
            console.print(converted_record)
            click.pause(info="Press any key to read next record")
        console.print("No more records")
        break


@cli.command("validate-records")
@click.option("-f", "--file", prompt=True)
def validate_records(file):
    reader = read_marc_records(file)
    n = 0
    while True:
        for record in reader:
            n += 1
            converted_record = get_record_input(record)
            record_type = get_material_type(r)
            if record_type == "monograph_record":
                try:
                    MonographRecord(**converted_record)
                    console.print(f"Record #{n} is valid.")
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = get_error_count(e)
                    console.print(
                        f"Record [record_number]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        console.print(f"\t{error[0]}: {error[1]}")
            else:
                try:
                    OtherMaterialRecord(**converted_record)
                    console.print(f"Record #{n} is valid.")
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = get_error_count(e)
                    console.print(
                        f"Record [record_number]#{n}[/] contains [error_count]{error_count} error(s)[/]"
                    )
                    for error in formatted_errors:
                        console.print(f"\t{error[0]}: {error[1]}")
            click.pause(info="Press any key to read and validate next record\n")
        console.print("No more records")
        break


@cli.command("validate-all")
@click.option("-f", "--file", prompt=True)
def validate_all(file):
    reader = read_marc_records(file)
    n = 0
    while True:
        console.print("\n\nChecking all records...")
        console.print("Printing results...\n\n")
        for record in reader:
            n += 1
            converted_record = get_record_input(record)
            control_number = converted_record["control_number"]
            console.print(
                f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/])"
            )
            try:
                MonographRecord(**converted_record)
                console.print("Validated successfully!")
            except ValidationError as e:
                formatted_errors = format_error_messages(e)
                error_count = get_error_count(e)
                console.print(
                    f"Record contains [error_count]{error_count} error(s)[/]:"
                )
                for error in formatted_errors:
                    console.print(f"\t{error[0]}: {error[1]}")
        console.print("Finished checking records.")
        break


@cli.command("validate-all-v2")
@click.option("-f", "--file", prompt=True)
def validate_all_v2(file):
    reader = read_marc_records(file)
    n = 0
    while True:
        console.print("\n\nChecking all records...")
        console.print("Printing results...\n\n")
        for r in reader:
            n += 1
            control_number = r["001"].data
            console.print(
                f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/])"
            )
            record_input = get_record_input(r)
            # item_input = get_item_input(r)
            try:
                # for item in item_input:
                #     Item(**item)
                Record(**record_input)
                console.print("Validated successfully!")
            except ValidationError as e:
                console.print(e.error_count())
                console.print(e.errors())
                # formatted_errors = format_error_messages(e)
                # error_count = get_error_count(e)
                # console.print(
                #     f"Record contains [error_count]{error_count} error(s)[/]:"
                # )
                # for error in formatted_errors:
                #     console.print(f"\t{error[0]}: {error[1]}")
        console.print("Finished checking records.")
        break


@cli.command("validate-all-v2")
@click.option("-f", "--file", prompt=True)
def validate_all_v3(file):
    reader = read_marc_records(file)
    n = 0
    while True:
        console.print("\n\nChecking all records...")
        console.print("Printing results...\n\n")
        for r in reader:
            n += 1
            control_number = r["001"].data
            console.print(
                f"\n\n[record_number]Record #{n}[/] (control_no [control_no]{control_number}[/])"
            )
            record_input = get_record_input(r)
            record_type = get_material_type(r)
            if record_type == "monograph_record":
                try:
                    m = MonographRecord(**record_input)
                    console.print(m)
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = get_error_count(e)
                    console.print(
                        f"Record contains [error_count]{error_count} error(s)[/]:"
                    )
                    for error in formatted_errors:
                        if len(error) == 3:
                            console.print(
                                f"\t{error[1]}: {error[2]} [[marc_field]{error[0]}[/]]"
                            )
                        else:
                            console.print(f"\t{error[0]}: {error[1]}")
            else:
                try:
                    m = OtherMaterialRecord(**record_input)
                    console.print(m)
                except ValidationError as e:
                    formatted_errors = format_error_messages(e)
                    error_count = get_error_count(e)
                    console.print(
                        f"Record contains [error_count]{error_count} error(s)[/]:"
                    )
                    for error in formatted_errors:
                        if len(error) == 3:
                            console.print(
                                f"\t{error[1]}: {error[2]} [[marc_field]{error[0]}[/]]"
                            )
                        else:
                            console.print(f"\t{error[0]}: {error[1]}")
        console.print("Finished checking records.")
        break
