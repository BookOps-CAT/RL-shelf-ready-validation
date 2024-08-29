from shelf_ready_validator.get_files_scratch_utils import get_vendor_files
from shelf_ready_validator.cli_commands import (
    validate_marc_file,
    write_vendor_sheet,
)

if __name__ == "__main__":
    auxam_output = validate_marc_file(
        "temp/auxam/AuxamInvoice240807F240828228.mrc", "AUXAM"
    )
    write_vendor_sheet(auxam_output, "auxam")
    # vendor_records = get_vendor_files("amalivre_lpa")
    # n = 1
    # for file in vendor_records:
    #     print(f"Validating file {n} of {len(vendor_records)}")
    #     output = validate_marc_file(file, "AUXAM")
    #     print(f"Writing output for file {n} of {len(vendor_records)}")
    #     write_vendor_sheet(output, "AUXAM")
    #     n += 1
