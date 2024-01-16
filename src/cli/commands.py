import click
from src.validate.models import Record
from src.validate.errors import convert_error_messages, get_error_count
from src.validate.translate import read_marc_to_dict, read_marc_records
from pydantic import ValidationError


@click.group()
def cli():
    pass


@click.command()
def intro():
    click.echo("MARC Record Validator")


@click.command()
@click.option("--file", prompt=True)
def read_records(file):
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
def read_records_to_dict(file):
    records = read_marc_to_dict(file)
    n = 0
    while True:
        for record in records:
            n += 1
            click.echo(f"Printing record {n}")
            click.echo(record)
            click.pause(info="Press any key to read next record")
        click.echo("No more records")
        break


@click.command
@click.option("--file", prompt=True)
def validate_records(input):
    try:
        Record(**input)
    except ValidationError as e:
        formatted_errors = convert_error_messages(e)
        error_count = get_error_count(e)
        return formatted_errors, error_count


cli.add_command(intro)
cli.add_command(read_records)
cli.add_command(read_records_to_dict)
cli.add_command(validate_records)

if __name__ == "__main__":
    cli()
