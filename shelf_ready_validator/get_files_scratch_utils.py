import os
import yaml
from typing import List
from file_retriever.connect import Client
from file_retriever.file import File


def connect(name: str) -> Client:
    client_name = name.upper()
    return Client(
        name=client_name,
        username=os.environ[f"{client_name}_USER"],
        password=os.environ[f"{client_name}_PASSWORD"],
        host=os.environ[f"{client_name}_HOST"],
        port=os.environ[f"{client_name}_PORT"],
    )


def get_vendor_files(vendor: str) -> List[File]:
    load_vendor_creds()
    vendor_dir = os.environ[f"{vendor.upper()}_DST"]
    all_files = []
    with connect("NSDROP") as client:
        file_list = client.list_file_info(time_delta=0, remote_dir=vendor_dir)
        for file in file_list:
            downloaded_file = client.get_file(file=file, remote_dir=vendor_dir)
            all_files.append(downloaded_file)
    return all_files


def load_vendor_creds() -> None:
    """Read yaml file and load vendor ftp/sftp credentials into environment variables"""
    config_path = os.path.join(
        os.environ["USERPROFILE"], ".cred/.sftp/connections.yaml"
    )
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        if config is None:
            raise ValueError("No credentials found in config file.")
        vendor_list = [
            i.split("_HOST")[0]
            for i in config.keys()
            if i.endswith("_HOST") and "NSDROP" not in i
        ]
        for k, v in config.items():
            os.environ[k] = v
        for vendor in vendor_list:
            os.environ[f"{vendor}_DST"] = f"NSDROP/vendor_records/{vendor.lower()}"
