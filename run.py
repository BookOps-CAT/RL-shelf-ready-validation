# from shelf_ready_validator.utils.get_files_scratch_utils import get_vendor_files
from rich import print
from shelf_ready_validator.utils.cli_commands import (
    validate_marc_file,
    # write_vendor_sheet,
)

if __name__ == "__main__":
    # auxam_output = validate_marc_file(
    #     "temp/auxam/AuxamInvoice240807F240828228.mrc", "AUXAM"
    # )
    # print(auxam_output)
    # leila_output = validate_marc_file("temp/31878.mrc", "LEILA")
    ev_output = validate_marc_file("temp/eastview/20050698_NYPL.mrc", "EASTVIEW")
    print(ev_output)
    # write_vendor_sheet(auxam_output, "auxam")
    # vendor_records = get_vendor_files("amalivre_lpa")
    # n = 1
    # for file in vendor_records:
    #     print(f"Validating file {n} of {len(vendor_records)}")
    #     output = validate_marc_file(file, "AUXAM")
    #     print(f"Writing output for file {n} of {len(vendor_records)}")
    #     write_vendor_sheet(output, "AUXAM")
    #     n += 1
