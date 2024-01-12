import click
from pymarc import MARCReader


# @click.command()
# @click.option("--file", prompt="Filename to read", confirmation_prompt=True)
# @click.argument("input", type=click.File("rb"))
# def read_validate_records():
#     with click.open_file("rl_sr_validation/records.json") as f:
#         click.echo("Reading records...")
#         records = json.loads(f.read())
#         n = 0

#         for record in records:
#             print(record)
# n += 1s
# try:
#     Record(**record)
#     print(f"Record {n} validates.")
# except ValidationError as e:
#     parsed_errors = parse_errors(e)
#     print(
#         f"Record {n} is not valid. This record contains {parsed_errors['error_count']} error(s)"
#     )
#     print(e.errors())


# @click.command()
# @click.option("--file", prompt="Filename to read", confirmation_prompt=True)
# @click.argument("input", type=click.File("rb"))
# def read_records():
# def reader(record):
#     with open ("temp/test.mrc", "rb") as fh:
#         reader = MARCReader(fh):
#         for record in reader:
#             yield record
