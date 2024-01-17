import click
from src.validate.models import Record
from src.validate.errors import convert_error_messages, get_error_count
from src.validate.translate import (
    read_marc_to_dict,
    read_marc_records,
    convert_to_input,
)
from pydantic import ValidationError


@click.group()
def cli():
    pass


@click.command()
def intro():
    click.echo("MARC Record Validator")


@click.command()
@click.option("-f", "--file", prompt=True)
def read_records_as_marc(file):
    records = read_marc_records(file)
    n = 0
    while True:
        for record in records:
            n += 1
            click.echo(f"Printing record {n}")
            click.echo(record)
            click.pause(info="Press any key to read next record")
        click.echo("No more records")
        break


@click.command()
@click.option("--file", prompt=True)
def read_records(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = convert_to_input(record)
            click.echo(f"Printing record {n}")
            click.echo(converted_record)
            click.pause(info="Press any key to read next record")
        click.echo("No more records")
        break


@click.command
@click.option("--file", prompt=True)
def validate_records(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        for record in records:
            n += 1
            converted_record = convert_to_input(record)
            click.echo(converted_record["item"]["material_type"])
            # click.echo(converted_record)
            click.echo(f"Validating record #{n}")
            try:
                Record(**converted_record)
                click.echo(f"Record #{n} is valid.")
            except ValidationError as e:
                formatted_errors = convert_error_messages(e)
                error_count = get_error_count(e)
                click.echo(f"Record #{n} contains {error_count} errors")
                click.echo("Listing errors...")
                click.echo(formatted_errors)
            click.pause(info="Press any key to read and validate next record")
        click.echo("No more records")
        break


cli.add_command(intro)
cli.add_command(read_records)
cli.add_command(read_records_as_marc)
cli.add_command(validate_records)

if __name__ == "__main__":
    cli()
