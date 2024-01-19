import click
from src.validate.models_v2 import Record, MonographRecord, ItemNYPLRL
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
            control_number = r.get("001")
            console.print(
                f"\n\n[record_number]Record #{n}[/record_number] (control_no [control_no]{control_number}[/control_no])"
            )
            try:
                Record(
                    MonographRecord(
                        material_type=r.get("949").get("z"),
                        bib_call_no=r.get("852").get("h"),
                        bib_vendor_code=r.get("901").get("a"),
                        lcc=r.get("050").get("a"),
                        invoice_date=r.get("980").get("a"),
                        invoice_price=r.get("980").get("b"),
                        invoice_shipping=r.get("980").get("c"),
                        invoice_tax=r.get("980").get("d"),
                        invoice_net_price=r.get("980").get("e"),
                        invoice_number=r.get("980").get("f"),
                        invoice_copies=r.get("980").get("g"),
                        order_price=r.get("960").get("s"),
                        order_location=r.get("960").get("s"),
                        order_fund=r.get("960").get("u"),
                        library="RL",
                        items=[
                            ItemNYPLRL(
                                item_call_tag=r.get("949").get("z"),
                                item_call_no=r.get("949").get("a"),
                                item_barcode=r.get("949").get("i"),
                                item_price=r.get("949").get("p"),
                                item_vendor_code=r.get("949").get("v"),
                                item_agency=r.get("949").get("h"),
                                item_location=r.get("949").get("l"),
                                item_type=r.get("949").get("t"),
                                library="RL",
                            )
                        ],
                    )
                )
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
