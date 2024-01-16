from pymarc import MARCReader


def read_marc_records(input):
    with open(input, "rb") as fh:
        reader = MARCReader(fh)
        for record in reader:
            dict_record = record.as_dict()
            yield dict_record


def translate_record(input):
    record = read_marc_records(input)
    # read the record and then output it to a dict that can be read into the validator
    return translated_record
