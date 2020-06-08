import sys
import configparser as cp
import ntpath
from executables.enums import Cloud
from WrapperAPI.CloudsAPI import *
from tkinter import messagebox


def main(directory):
    """
    This code is converted to exe file that uploads file from the
    file explorer to the cloud

    :param directory: The directory of the file that is uploaded
    """
    path, name = ntpath.split(directory)
    account_path = directory.split('\\')[0] + "\\" + directory.split('\\')[1] + "\\account.ini"
    config = cp.ConfigParser()
    config.read(account_path)
    cloud_type = config['accountSettings']['type']
    username = config['accountSettings']['username']

    if cloud_type == Cloud.GoogleDrive.value:
        creds = config['accountSettings']['credentials']
        service = GoogleDriveCloud(creds)
        remote_path = path.split('\\', 2)[2]
        remote_files = service.get_files_names(remote_path)[remote_path]
        if name in remote_files:
            messagebox.showerror("Error", "The {0} file already exists in the current directory.".format(name))
        else:
            service.upload_file(directory, True, remote_path)
            messagebox.showinfo("Success", "The file {0} was succesfuly uploaded to your Google Drive account".
                                format(name))

    elif cloud_type == Cloud.Dropbox.value:
        token = config['accountSettings']['tokenkey']
        service = DropboxCloud(token)
        remote_path = path.split('\\', 2)[2]
        remote_files = service.get_files_names_ordered("/" + remote_path)["/" + remote_path]
        if name in remote_files:
            messagebox.showerror("Error", "The {0} file already exists in the current directory.".format(name))
        else:
            service.upload_file(directory, name, remote_path + "/")
            messagebox.showinfo("Success", "The file {0} was succesfuly uploaded to your Dropbox account".format(name))

    elif cloud_type == Cloud.MegaUpload.value:
        password = config['accountSettings']['password']
        service = MegaUploadCloud(username, password)
        remote_path = path.split('\\', 2)[2]
        remote_files = service.get_files_names(remote_path)
        if name in remote_files:
            messagebox.showerror("Error", "The {0} file already exists in the current directory.".format(name))
        else:
            service.upload(directory, remote_path + "/" + name)
            messagebox.showinfo("Success", "The file {0} was succesfuly uploaded to your Mega Upload account".
                                format(name))


if __name__ == '__main__':
    main(sys.argv[1])
