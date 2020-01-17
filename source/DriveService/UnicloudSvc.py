import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
from WrapperAPI.CloudsAPI import *
from WindowsManagement.VirtualDisk import MappedDrive


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "UnicloudSvc"
    _svc_display_name_ = "Unicloud Drive Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def svc_stop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def svc_do_run(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    @staticmethod
    def main():
        google_drive_service = GoogleDriveCloud()
        dropbox_service = DropboxCloud("q8AOvG028RAAAAAAAAAARl4cbDhkbW1k0CX9w09-9zce7Aoheti6kRSqXiOaFfeU")
        mega_upload_service = MegaUploadCloud("nimni.project@gmail.com", "0522724447")
        while True:
            GD_files = google_drive_service.get_files_metadata()

            MU_files = mega_upload_service.get_files_names()
            DB_files = dropbox_service.get_files_names()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
