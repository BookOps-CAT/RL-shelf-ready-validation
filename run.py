from rich import print
from shelf_ready_validator.get_files_scratch_utils import get_vendor_files
from shelf_ready_validator.cli_commands import read_validate_file

if __name__ == "__main__":
    # this is what the vendor_file_cli will do
    leila_files = get_vendor_files("leila")

    # this fits in after get_file and before put_file in the vendor_file_cli
    leila_output = read_validate_file(leila_files[0])
    print(leila_output)
    # this is what the vendor_file_cli will do
    ev_files = get_vendor_files("eastview")

    # this fits in after get_file and before put_file in the vendor_file_cli
    ev_output = read_validate_file(ev_files[0])
    print(ev_output)
    # leila_errors = []
    # for l_output in leila_output:
    #     for error in l_output["errors"]:
    #         leila_errors.append(error)
    # leila_type_counter: Counter = Counter()
    # for error in leila_errors:
    #     leila_type_counter[error["error_type"]] += 1
    # print(leila_type_counter)

    # amalivre_lpa_files = get_vendor_files("amalivre_lpa")
    # amalivre_lpa_output = read_validate_file(amalivre_lpa_files[0])
    # aux_errors = []
    # for a_output in amalivre_lpa_output:
    #     for error in a_output["errors"]:
    #         aux_errors.append(error)
    # aux_counter: Counter = Counter()
    # for error in aux_errors:
    #     aux_counter[error["error_type"]] += 1
    # print(aux_counter)

    # ev_files = get_vendor_files("eastview")
    # ev_output = read_validate_file(ev_files[0])
    # ev_errors = []
    # for output in ev_output:
    #     for error in output["errors"]:
    #         ev_errors.append(error)
    # ev_counter: Counter = Counter()
    # for error in ev_errors:
    #     ev_counter[error["error_type"]] += 1
    # print(ev_counter)
