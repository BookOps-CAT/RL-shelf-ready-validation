from shelf_ready_validator.utils import read_marc_records, marc2json

def test_marc2json(file: str)
    records = read_marc_records("tests/test.mrc")
    for record in records:
        print(marc2json(record))