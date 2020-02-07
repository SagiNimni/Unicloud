import configparser as cp
import shutil
import os
from executables.enums import Cloud
from WrapperAPI.CloudsAPI import *
from definitions import SCRIPTS_DIR, CONFIG_DIR


def establishUnicloudConnectionToFolder(directory, username, credentials, cloud_type):
    os.mkdir(directory)
    config = cp.ConfigParser()
    config.add_section("accountSettings")
    with open(directory + "/account.ini", 'w+') as f:
        if Cloud.Dropbox.name == cloud_type:
            config.set("accountSettings", "type", Cloud.Dropbox.value)
            config.set("accountSettings", "tokenKey", credentials)
            config.set("accountSettings", "username", username)
            config.write(f)
            _BuildDropboxDirectories_(directory, credentials)
        elif Cloud.GoogleDrive.name == cloud_type:
            credentials_directory = directory + "/credentials.json"
            config.set("accountSettings", "type", Cloud.GoogleDrive.value)
            config.set("accountSettings", "credentials", credentials_directory)
            config.set("accountSettings", "username", username)
            config.write(f)
            shutil.move(credentials, credentials_directory)
            os.system("attrib +h {0}".format(credentials_directory))
            _BuildGoogleDriveDirectories_(directory, credentials_directory)
        elif Cloud.MegaUpload.name == cloud_type:
            config.set("accountSettings", "type", Cloud.MegaUpload.value)
            config.set("accountSettings", "password", credentials)
            config.set("accountSettings", "username", username)
            config.write(f)
            _BuildMegaUploadDirectories_(directory, username=username, password=credentials)
        f.close()
        os.system("attrib +h {0}".format(directory + "/account.ini"))


def _BuildGoogleDriveDirectories_(directory, credentials):
    service = GoogleDriveCloud(credentials)
    files_list = service.get_files_metadata()
    for file in files_list:
        file_name = file[0]
        if len(file_name.split('.')) == 2:
            parent_id = file[2]
            remote_path = service.get_file_path(file_name, parent_id)
            local_path = directory + "/" + remote_path
            os.makedirs(local_path)
            _CreateVirtualFile_(local_path, 'GD', remote_path)
    print("done")


def _BuildMegaUploadDirectories_(directory, username=None, password=None, remote_path=None, service=None):
    if not service:
        service = MegaUploadCloud(username, password)
    files_list = service.get_files_names(remote_path)
    for file in files_list:
        if file != '':
            if len(file.split('.')) == 2:
                if not remote_path:
                    local_path = directory + "/" + file
                    os.makedirs(local_path)
                    _CreateVirtualFile_(local_path, 'MU', file)
                else:
                    local_path = directory + "/" + remote_path + "/" + file
                    os.makedirs(local_path)
                    _CreateVirtualFile_(local_path, 'MU', remote_path + "/" + file)
            else:
                if not remote_path:
                    _BuildMegaUploadDirectories_(directory, remote_path=file, service=service)
                else:
                    _BuildMegaUploadDirectories_(directory, remote_path=remote_path + "/" + file, service=service)


def _BuildDropboxDirectories_(directory, token_key):
    service = DropboxCloud(token_key)
    files_list = service.get_files_names()
    for file in files_list:
        file = file['name']
        local_path = directory + file
        os.makedirs(local_path)
        _CreateVirtualFile_(local_path, 'DB', file)


def _CreateVirtualFile_(directory, drive_type, remote_path):
    config = cp.ConfigParser()
    with open(directory + "/prop.ini", 'w+') as f:
        section = "DriveSettings"
        config.add_section(section)
        config.set(section, 'type', drive_type)
        config.set(section, 'path', remote_path)
        config.write(f)
        f.close()
        os.system("attrib +h {0}".format(directory + "/prop.ini"))

    cmd = [SCRIPTS_DIR + '\\editDesktopinf.vbs', directory, CONFIG_DIR + '\\cloud.ico']
    os.system("cscript {0}\\editDesktopinf.vbs {1} {2}\\cloud.ico".format(SCRIPTS_DIR, directory.replace('/', '\\'),
                                                                          CONFIG_DIR))
    os.system("attrib +s +h {0}".format(directory + '/desktop.ini'))
    os.system("attrib +s {0}".format(directory))

