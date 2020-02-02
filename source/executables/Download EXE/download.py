import configparser as cp
import sys
import os
import shutil
import ntpath
import tkinter
from tkinter import messagebox
from executables.enums import Cloud
from WrapperAPI.CloudsAPI import GoogleDriveCloud, MegaUploadCloud, DropboxCloud
from executables.utillty import handle_remove_readonly


def main(directory):
    config = cp.ConfigParser()
    prop_path = directory + "\\prop.ini"
    if os.path.exists(prop_path):
        config.read(prop_path)
        properties = {'type': config['DriveSettings']['type'], 'path': config['DriveSettings']['path']}
        try:
            config = cp.ConfigParser()
            root_folder = directory.split('\\', 2)[0] + "\\" + directory.split("\\", 2)[1]
            config.read(root_folder + "\\account.ini")
            if properties['type'] == Cloud.GoogleDrive.value:
                account_properties = {"credentials": config["accountSettings"]["credentials"]}
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = GoogleDriveCloud(account_properties['credentials'])
                service.download_file(properties['path'], directory + '\\')
            elif properties['type'] == Cloud.MegaUpload.value:
                account_properties = {'username': config["accountSettings"]["username"],
                                      'password': config["accountSettings"]["password"]}
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = MegaUploadCloud(account_properties['username'], account_properties['password'])
                service.download(properties['path'], directory)
            elif properties['type'] == Cloud.Dropbox.value:
                account_properties = {'token key': config["accountSettings"]["tokenkey"]}
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = DropboxCloud(account_properties['token key'])
                service.download_file(properties['path'], directory)
        except Exception as e:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("Error", e)
    else:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("Error", "The prop file is missing.")


if __name__ == '__main__':
    main(sys.argv[1])
