import os
import time
import paramiko
import traceback
from datetime import datetime
from stat import S_ISDIR, S_ISREG
from scp import SCPClient, SCPException
from utils.common import LOGGER, FILETYPE
from hurry.filesize import size
from paramiko.ssh_exception import SSHException, AuthenticationException
from paramiko import SFTPAttributes


class SSHClient:

    QUERY_RAM_STATS = 'free -g'
    QUERY_DISK_STATS = 'df -h /'
    QUERY_CPU_STATS = ''
    QUERY_SYSTEMD_SERVICES = 'systemctl list-units --type=service | grep systemd'

    def __init__(self, ip: str, username: str, password: str):
        self.ip = ip
        self.username = username
        self.password = password
        self.client = None

    @property
    def connection(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.RejectPolicy())
            client.connect(hostname=self.ip, username=self.username, password=self.password, timeout=5000)
            return_value = client
        except AuthenticationException:
            msg = "Authentication Error"
            LOGGER.error(msg)
            return_value = msg
        except SSHException:
            msg = f"SSH Connection Error, check your credentials"
            LOGGER.error(msg)
            return_value = msg
        except Exception as e:
            msg = f"Unexpected error occurred while connecting to host: {self.ip}"
            LOGGER.error(msg)
            return_value = msg
        return return_value if return_value else None

    @property
    def scp(self):
        conn = self.connection
        return SCPClient(conn.get_transport())

    def disconnect(self):
        LOGGER.info(f"Closing connection to remote host: {self.ip}")
        if self.connection:
            self.connection.close()
        if self.scp:
            self.scp.close()

    def is_connected(self) -> bool:
        return True if self.connection else False

    def is_path_exists(self, path: str):
        try:
            sftp = self.connection.open_sftp()
            path = sftp.stat(path)
            sftp.close()
            return_value = True
        except FileNotFoundError:
            return_value = False
        return return_value

    def get_files_and_folders_stats_in_remote_dir(self, remote_dir: str) -> [str]:
        keys = ['file_name', 'file_path',  'type', 'permissions', 'size', 'last_modified']
        sftp_client = self.connection.open_sftp()
        LOGGER.info(f"Opening sftp connection to get files and folders in {remote_dir}")
        files_stats_list = list()
        for entry in sftp_client.listdir_attr(remote_dir):
            file_stats = SSHClient._get_file_stats(remote_dir, keys, entry)

            files_stats_list.append(file_stats)
        sftp_client.close()
        return files_stats_list

    @staticmethod
    def _get_file_stats(remote_dir: str, keys: [str],  entry: SFTPAttributes):
        mode = entry.st_mode
        file_permissions = entry.longname.split()[0]
        datetime_obj = datetime.fromtimestamp(entry.st_mtime)
        last_modified = datetime_obj.strftime("%Y-%m-%d %H:%M")
        file_size_str = size(entry.st_size)
        file_type = FILETYPE.FILE.name if S_ISREG(mode) else FILETYPE.DIRECTORY.name
        file_path = os.path.join(remote_dir, entry.filename)
        return dict(zip(keys, [entry.filename, file_path, file_type, file_permissions, file_size_str, last_modified]))

    def transfer_files(self, local_path: str, remote_path: str, host_to_local: bool, recursive: bool):
        try:
            if host_to_local:
                LOGGER.info(f"Transfering files from {remote_path} to {local_path}")
                self.scp.get(remote_path=remote_path, local_path=local_path, recursive=recursive)
            else:
                LOGGER.info(f"Transfering files from {local_path} to {remote_path}")
                self.scp.put(files=local_path, remote_path=remote_path, recursive=recursive)
        except SCPException as e:
            LOGGER.error(traceback.format_exc())
            LOGGER.error("SCP ERROR, Failed to transfer files")
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            LOGGER.error("General ERROR, Failed to transfer files")

    def run_command(self, command: str) -> [[str], [str]]:
        stdin, stdout, stderr = self.connection.exec_command(command)
        formatted_stdout = stdout.readlines()
        formatted_stderr = stderr.readlines()
        return formatted_stdout, formatted_stderr

    def _get_ram_stats(self) -> dict:
        stdout, stderr = self.run_command(SSHClient.QUERY_RAM_STATS)
        ram_stats = {key: "" for key in ['total', 'used', 'free', 'in_cache', 'avail']}
        if len(stdout) > 1:
            _, total, used, free, shared, in_cache, avail = stdout[1].split()
            ram_stats["free"] = free
            ram_stats["total"] = total
            ram_stats["used"] = used
            ram_stats["in_cache"] = in_cache
            ram_stats["avail"] = avail
        return ram_stats

    def _get_disk_stats(self, dir_paths: [str]) -> [dict]:
        stdout, stderr = self.run_command(SSHClient.QUERY_DISK_STATS)
        keys = ['disk_name', 'total', 'used', 'free', 'precentage', 'mounted_path']
        disk_stats_list = list()
        if len(stdout) > 1:
            mounted_disks = SSHClient._get_mounted_disks(stdout, dir_paths)
            for mounted_disk in mounted_disks:
                disk_stats = dict(zip(keys, mounted_disk.split()))
                disk_stats_list.append(disk_stats)
        return disk_stats_list

    @staticmethod
    def _get_mounted_disks(stdout: [str], dir_paths: [str]) -> [str]:
        return [line.strip() for dir_path in dir_paths for line in stdout if dir_path in line]

    def get_system_stats(self, dir_paths: [str]) -> [[dict], dict]:
        disk_stats = self._get_disk_stats(dir_paths)
        ram_stats = self._get_ram_stats()
        return disk_stats, ram_stats

    def stop_services(self, services_names: [str]):
        pass

    def start_services(self, services_names: [str]):
        pass

    def list_services(self):
        stdout, stderr = self.run_command(SSHClient.QUERY_SYSTEMD_SERVICES)
        keys = ['service_name', 'loaded', 'active', 'status', 'description']
        services_list = [dict(zip(keys, line.split())) for line in stdout]
        return services_list
