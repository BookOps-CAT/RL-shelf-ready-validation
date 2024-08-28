from rich import print
from shelf_ready_validator.utils import (
    get_vendor_files,
)
from shelf_ready_validator.cli_commands import read_validate_file

if __name__ == "__main__":
    # this is what the vendor_file_cli will do
    vendor_files = get_vendor_files("leila")
    # this fits in after get_file and before put_file in the vendor_file_cli
    # for file in vendor_files:
    validation_output = read_validate_file(vendor_files[0])
    print(validation_output)
