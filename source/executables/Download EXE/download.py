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
            if properties['type'] == Cloud.GoogleDrive.value:
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = GoogleDriveCloud()
                service.download_file(properties['path'], directory + '\\')
            elif properties['type'] == Cloud.MegaUpload.value:
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = MegaUploadCloud("nimni.project@gmail.com", "0522724447")
                service.download(properties['path'], directory)
            elif properties['type'] == Cloud.Dropbox.value:
                shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)
                directory, tail = ntpath.split(directory)
                service = DropboxCloud("q8AOvG028RAAAAAAAAAARl4cbDhkbW1k0CX9w09-9zce7Aoheti6kRSqXiOaFfeU")
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
