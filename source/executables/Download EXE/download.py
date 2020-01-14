import configparser as cp
import sys
import os
import shutil
import ntpath
from executables.enums import Cloud
from WrapperAPI.CloudsAPI import GoogleDriveCloud, MegaUploadCloud, DropboxCloud


def main(directory):
    config = cp.ConfigParser()
    prop_path = directory + "\\prop.ini"
    if os.path.exists(prop_path):
        config.read(prop_path)
        properties = {'type': config['DriveSettings']['type'], 'path': config['DriveSettings']['path']}
        if properties['type'] == Cloud.GoogleDrive.value:
            shutil.rmtree(directory, ignore_errors=True)
            directory, tail = ntpath.split(directory)
            service = GoogleDriveCloud()
            service.download_file(properties['path'], directory + '\\')
        elif properties['type'] == Cloud.MegaUpload.value:
            shutil.rmtree(directory, ignore_errors=True)
            directory, tail = ntpath.split(directory)
            service = MegaUploadCloud("nimni.project@gmail.com", "0522724447")
            service.download(properties['path'], directory)
        elif properties['type'] == Cloud.Dropbox.value:
            shutil.rmtree(directory, ignore_errors=True)
            directory, tail = ntpath.split(directory)
            service = DropboxCloud("q8AOvG028RAAAAAAAAAARl4cbDhkbW1k0CX9w09-9zce7Aoheti6kRSqXiOaFfeU")
            service.download_file(properties['path'], directory)
    else:
        raise NotADirectoryError("This directory does not exist, or has been removed")


if __name__ == '__main__':
    main(sys.argv[1])
