import sys
import configparser as cp
from os import walk
from tkinter import messagebox
from executables import Cloud
from BuildDiskDrive.buildSkeleton import _CreateVirtualFile_
from WrapperAPI.CloudsAPI import *


def reload(folder_generator: iter, remote_files, drive_type):
    try:
        while True:
            directory, local_folders, local_files = folder_generator.__next__()
            head, tail = ntpath.split(directory)
            if len(tail.split('.')) == 1:
                local_files.extend(local_folders)
                try:
                    if drive_type == Cloud.Dropbox.value:
                        remote_path = ('/' + directory.split('\\', 2)[2]).replace('\\', '/')
                    else:
                        remote_path = (directory.split('\\', 2)[2]).replace('\\', '/')
                except IndexError:
                    if drive_type == Cloud.Dropbox.value:
                        remote_path = '/'
                    else:
                        remote_path = ''
                s1 = set(remote_files[remote_path])
                s2 = set(local_files)
                new_folders = s1.difference(s2)
                for file in new_folders:
                    if len(file.split('.')) == 2:
                        os.makedirs(directory + "\\" + file)
                        _CreateVirtualFile_(directory + "\\" + file, drive_type, remote_path + "\\" + file)
                    else:
                        os.mkdir(directory + "/" + file)
                        reload(walk(directory + "\\" + file), remote_files, drive_type)
    except StopIteration:
        return


def main(directory: str):
    account_path = directory.split('\\')[0] + "\\" + directory.split('\\')[1] + "\\account.ini"
    config = cp.ConfigParser()
    config.read(account_path)
    cloud_type = config['accountSettings']['type']
    username = config['accountSettings']['username']

    if cloud_type == Cloud.MegaUpload.value:
        password = config['accountSettings']['password']
        try:
            remote_path = directory.split('/', 2)[2]
        except IndexError:
            remote_path = ''
        service = MegaUploadCloud(username, password)
        remote_files = service.get_all_subdirs_files_names(remote_path)

        folder_data = walk(directory)
        reload(folder_data, remote_files, cloud_type)
        messagebox.showinfo("Success", "Reload finished successfully.")

    elif cloud_type == Cloud.GoogleDrive.value:
        creds = config['accountSettings']['credentials']
        service = GoogleDriveCloud(creds)
        try:
            remote_path = directory.split('/', 2)[2]
        except IndexError:
            remote_path = None
        remote_files = service.get_files_names(remote_path)

        folder_data = walk(directory)
        reload(folder_data, remote_files, cloud_type)
        messagebox.showinfo("Success", "Reload finished successfully.")

    elif cloud_type == Cloud.Dropbox.value:
        token = config['accountSettings']['tokenkey']
        service = DropboxCloud(token)
        try:
            remote_path = directory.split('/', 2)[2]
        except IndexError:
            remote_path = ''
        remote_files = service.get_files_names_ordered(remote_path)

        folder_data = walk(directory)
        reload(folder_data, remote_files, cloud_type)
        messagebox.showinfo("Success", "Reload finished successfully.")


if __name__ == '__main__':
    main(sys.argv[1])
