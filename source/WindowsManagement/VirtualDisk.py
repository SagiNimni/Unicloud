import subprocess
import winreg
import os
from WindowsManagement.errors import DriveLetterUsedError


class MappedDrive:
    """
    This class is responsible for the mapped drive that will store the data of Unicloud.
    It includes build and delete function for the user.
    """
    PSUBST_PATH = "~/PycharmProjects/UniCloud-VC/source/WindowsManagement/diskScripts/"

    def __init__(self, letter: str, drive_directory: str, name):
        """
        This method is building a mapped drive in the current user.
        It gives the drive a name and icon.
        If the drive already exists it only returns the MappedDrive object without creating a new drive

        :param letter: The mapped drive letter(for example U:)
        :param drive_directory:  The directory that the drive is mapped to
        :param name: The name of the new mapped drive
        """
        mapped_drives = (os.popen('subst').read()).split('\n')
        try:
            for d in mapped_drives:
                drive_letter = d.split("\\")[0]
                drive_path = d.split(" ")[2]
                if drive_letter == letter:
                    if drive_path == drive_directory:
                        self.letter = letter
                        self.drive_directory = drive_directory
                        return
                    else:
                        raise DriveLetterUsedError("{0} is already used by another drive".format(letter))
        except IndexError:
            cmd = [MappedDrive.PSUBST_PATH + "psubst.bat", letter, drive_directory, "/P"]
            subprocess.run(cmd)
            self.letter = letter
            self.drive_directory = drive_directory
            print("The directory was successfully mapped")
            os.system("attrib +s {0}\\*.* /d /s".format(letter))
            self._rename_mapped_drive_(name)
            self._change_icon_()
            self._add_context_menu_()

    def delete_mapped_drive(self):
        """
        This method purpose is to delete the current drive instance.
        It deletes the drive and it's settings from the computer registry and therefor the drive is deleted.

        :return: None
        """
        cmd = [MappedDrive.PSUBST_PATH + "psubst.bat", self.letter, "/D", "/P"]
        subprocess.run(cmd)
        subkey_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DriveIcons\{0}\DefaultIcon'. \
            format(self.letter[:-1])
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
        subkey_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DriveIcons\{0}'.format(self.letter[:-1])
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
        print("The virtual drive was successfully deleted")

    def _rename_mapped_drive_(self, name: str):
        """
        This method starts a VBscript that changes the drive name

        :param name: The new name of the drive
        :return: None
        """
        os.system("cscript {0}rename.vbs {1} {2}".format(MappedDrive.PSUBST_PATH, self.letter, name))
        print("Drive was successfully renamed to {0}".format(name))

    def _change_icon_(self, icon_path=r'"C:\Users\nimni\PycharmProjects\UniCloud\configuration\cloud.ico"'):
        """
        This method changes the registry in order to change the mapped drive icon.
        It might need user permission in order to complete it's task.

        :param icon_path: A path for the .ico file that will be used as the drive's icon
        :return: None
        """
        subkey_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\DriveIcons\{0}\DefaultIcon'.\
            format(self.letter[:-1])
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, icon_path)
        key.Close()

    def _add_context_menu_(self, menu_icon=r"C:\Users\nimni\PycharmProjects\UniCloud\configuration\cloud.ico"):
        # create context menu with sub commands
        subkey_path = r'Directory\Shell\Unicloud'
        key = winreg.CreateKeyEx(winreg.HKEY_CLASSES_ROOT, subkey_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'AppliesTo', 0, winreg.REG_SZ, self.letter)
        winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, menu_icon)
        winreg.SetValueEx(key, 'SubCommands', 0, winreg.REG_SZ, "download")
        winreg.SetValueEx(key, 'Position', 0, winreg.REG_SZ, "Top")

        # create sub commands
        def make_sub_command(command_name, command, command_icon):
            subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\{0}'.format(command_name)
            hkey = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(hkey, 'Icon', 0, winreg.REG_SZ,
                              r'C:\Users\nimni\PycharmProjects\UniCloud\configuration\{0}'.format(command_icon))
            subkey = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\{0}\command'.format(command_name)
            hkey = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, subkey, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(hkey, '', 0, winreg.REG_SZ, command)

        make_sub_command("download", r'"C:\Users\nimni\PycharmProjects\UniCloud\executables\Download EXE\dist\download\
                            download.exe" "%1"', 'download.ico')
