import paramiko
import os.path
import json
from rich import print
from datetime import datetime, timedelta


class sftpConnection:
    """
    a class to define an SFTP connection for vendors
    """

    def __init__(self, vendor: str):
        self.vendor = vendor

    def _open_ssh_creds(self):
        ssh_cred_path = os.path.join(
            os.environ["USERPROFILE"], f".cred/.sftp/{self.vendor}.json"
        )
        ssh_cred_file = open(ssh_cred_path, "r")
        ssh_creds = json.load(ssh_cred_file)
        return ssh_creds

    def _create_sftp_client(self):
        ssh_creds = self._open_ssh_creds()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(
            hostname=ssh_creds["host"],
            port=ssh_creds["port"],
            username=ssh_creds["username"],
            password=ssh_creds["password"],
        )
        sftp_client = ssh_client.open_sftp()
        return sftp_client

    def get_records(self):
        """
        Gets all records from a vendor sftp site
        """
        filepath = self._open_ssh_creds()["filepath"]
        sftp_client = self._create_sftp_client()
        local = os.path.join(
            os.environ["USERPROFILE"],
            f"github/RL-shelf-ready-validation/temp/{self.vendor}/",
        )
        dir_list = sftp_client.listdir(filepath)
        local_file_list = []
        sftp_client.chdir(filepath)
        for file in dir_list:
            sftp_client.get(file, f"{local + file}")
            local_file_list.append(file)
        sftp_client.close()
        return local_file_list

    def list_all_files(self):
        """
        Checks vendor sftp site and lists each file
        """
        today = datetime.now()
        filepath = self._open_ssh_creds()["filepath"]
        sftp_client = self._create_sftp_client()
        local = os.path.join(
            os.environ["USERPROFILE"],
            f"github/RL-shelf-ready-validation/temp/{self.vendor}/",
        )
        dir_list = sftp_client.listdir(filepath)
        sftp_client.chdir(filepath)
        for file in dir_list:
            local_path = local + file
            file_data = sftp_client.stat(file)
            update_date = datetime.fromtimestamp(file_data.st_mtime)
            print(f"{file} was created {(today - update_date).days} days ago on {update_date.strftime('%Y-%m-%d')}")
        sftp_client.close()

    def get_recent_records(self):
        """
        Checks vendor sftp site and lists each file.
        If a file has been created within the last week it will be downloaded
        """
        today = datetime.now()
        filepath = self._open_ssh_creds()["filepath"]
        sftp_client = self._create_sftp_client()
        local = os.path.join(
            os.environ["USERPROFILE"],
            f"github/RL-shelf-ready-validation/temp/{self.vendor}/",
        )
        dir_list = sftp_client.listdir(filepath)
        todays_files = []
        sftp_client.chdir(filepath)
        for file in dir_list:
            local_path = local + file
            file_data = sftp_client.stat(file)
            update_date = datetime.fromtimestamp(file_data.st_mtime)
            if update_date >= today - timedelta(days=7):
                sftp_client.get(file, local_path)
                print(f"{file} is new today, {today.strftime('%Y-%m-%d')}")
            todays_files.append(local_path)
        sftp_client.close()
        return todays_files
    
    def list_recent_records(self):
        """
        Checks vendor sftp site and lists each file.
        If a file has been created within the last week it will be downloaded
        """
        today = datetime.now()
        filepath = self._open_ssh_creds()["filepath"]
        sftp_client = self._create_sftp_client()
        local = os.path.join(
            os.environ["USERPROFILE"],
            f"github/RL-shelf-ready-validation/temp/{self.vendor}/",
        )
        dir_list = sftp_client.listdir(filepath)
        sftp_client.chdir(filepath)
        for file in dir_list:
            local_path = local + file
            file_data = sftp_client.stat(file)
            update_date = datetime.fromtimestamp(file_data.st_mtime)
            if update_date >= today - timedelta(days=7):
                print(f"{file} is new today ({today.strftime('%Y-%m-%d')}) and was created on {update_date.strftime('%Y-%m-%d')}")
        sftp_client.close()