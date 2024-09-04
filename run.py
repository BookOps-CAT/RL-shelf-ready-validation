# from shelf_ready_validator.utils.get_files_scratch_utils import get_vendor_files
import os
from rich import print
from shelf_ready_validator.utils.cli_commands import (
    validate_marc_file,
    write_vendor_sheet,
)

if __name__ == "__main__":
    aux_sasb = os.listdir("temp/auxam")
    aux_lpa = os.listdir("temp/auxam_lpa")
    aux_schomburg = os.listdir("temp/auxam_schomburg")
    leila = os.listdir("temp/leila")
    ev = os.listdir("temp/eastview")
    # for file in aux_sasb:
    #     auxam_sasb_output = validate_marc_file(f"temp/auxam/{file}", "AUXAM")
    #     print(auxam_sasb_output)
    #     write_vendor_sheet(auxam_sasb_output, "testing")
    for file in aux_schomburg:
        aux_schomburg_output = validate_marc_file(
            f"temp/auxam_schomburg/{file}", "AUXAM"
        )
        print(aux_schomburg_output)
        write_vendor_sheet(aux_schomburg_output, "testing")
