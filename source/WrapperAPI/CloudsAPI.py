from __future__ import print_function
import pickle
import os.path
import os
import io
import ntpath
import subprocess
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import dropbox
import dropbox.files
from WrapperAPI import convert
from WrapperAPI import utility
from WrapperAPI import errors as e
from tkinter import ttk
from definitions import MEGA_BASH_DIR


class DropboxCloud:  # TODO implement delete functions
    """
     This class contains the root service of the dropbox API and through that we can access and modify the dropbox
     account.
     It implements upload, download, files_list and storage_status functions which make it possible to access dropbox
     easily.
     """
    CHUNK_SIZE = 4 * 1024 * 1024

    def __init__(self, token_code):
        self.token_code = token_code
        self.dbx = dropbox.Dropbox(self.token_code)
        print("Successfully Initialized Dropbox API")

    def get_files_names_ordered(self, path=""):
        files_list = {}
        result = self.dbx.files_list_folder(path=path)
        files = self._process_folder_entries_({}, result.entries)
        for key in files.keys():
            path, name = ntpath.split(key)
            if path not in files_list.keys():
                files_list.update({path: [name]})
            else:
                files_list[path].append(name)
            if path != '/':
                sub_path, dir_name = ntpath.split(path)
                if sub_path not in files_list.keys():
                    files_list.update({sub_path: [dir_name]})
                else:
                    if dir_name not in files_list[sub_path]:
                        files_list[sub_path].append(dir_name)
        return files_list

    def get_files_names(self, path=""):
        files_list = []
        result = self.dbx.files_list_folder(path=path)
        files = self._process_folder_entries_({}, result.entries)
        for key in files.keys():
            files_list.append({"name": key})
        return files_list

    def _process_folder_entries_(self, current_state, entries):
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                current_state[entry.path_lower] = entry
            elif isinstance(entry, dropbox.files.FolderMetadata):
                folder_result = self.dbx.files_list_folder(path=entry.path_lower)
                current_state.update(self._process_folder_entries_(current_state, folder_result.entries))
            elif isinstance(entry, dropbox.files.DeletedMetadata):
                current_state.pop(entry.path_lower, None)
        print(current_state.keys())
        return current_state

    def upload_file(self, directory: str, name: str, path=""):
        file_size = os.path.getsize(directory)
        with open(directory, 'rb') as f:
            if file_size <= self.CHUNK_SIZE:
                print('/{0}{1}'.format(path, name))
                self.dbx.files_upload(f.read(), '/{0}{1}'.format(path, name))
                print("Successfully uploaded {0} to dropbox".format(name))
            else:
                upload_session_start_result = self.dbx.files_upload_session_start(f.read(self.CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path='/{0}{1}'.format(path, name))
                while f.tell() < file_size:
                    if file_size - f.tell() < self.CHUNK_SIZE:
                        self.dbx.files_upload_session_finish(f.read(self.CHUNK_SIZE), cursor, commit)
                    else:
                        self.dbx.files_upload_session_append(f.read(self.CHUNK_SIZE), cursor.session_id, cursor.offset)
                        cursor.offset = f.tell()
                print("Successfully uploaded {0} to dropbox".format(name))

    def upload_folder(self, directory: str, name: str, path=""):
        dropbox_folder_path = path + name + "/"
        self.dbx.files_create_folder('/{0}{1}'.format(path, name))
        for filename in os.listdir(directory):
            file_directory = directory + '/' + filename
            if os.path.isfile(file_directory):
                self.upload_file(file_directory, filename, dropbox_folder_path)
            elif os.path.isdir(directory):
                self.upload_folder(file_directory, filename, dropbox_folder_path)

    def download_file(self, path, directory):
        directory = directory.replace(os.sep, '/')
        head, name = ntpath.split(path)
        self.dbx.files_download_to_file(directory + "/" + name, path)
        print("Successfully downloaded {0} to {1}".format(name, directory))

    def download_folder(self, path, directory):
        folder_files = self.get_files_names(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            for file in folder_files:
                self.download_file(file["name"], directory)
        else:
            raise IsADirectoryError

    def storage_status(self, mute=False):
        if mute is True:
            utility.block_print()
        usage = self.dbx.users_get_space_usage()
        gb1, mb1 = convert.convert_bytes_to_gb(usage.allocation.get_individual().allocated)
        capacity = {"GB": gb1, "MB": mb1}
        print("Capacity: " + str(gb1) + "GB &", str(mb1) + "MB")
        gb2, mb2 = convert.convert_bytes_to_gb(usage.used)
        used_space = {"GB": gb2, "MB": mb2}
        print("Used Space: " + str(gb2) + "GB &", str(mb2) + "MB")
        gb3, mb3 = convert.convert_bytes_to_gb(usage.allocation.get_individual().allocated - usage.used)
        free_space = {"GB": gb3, "MB": mb3}
        print("Free space:", str(gb3) + "GB &", str(mb3) + "MB")
        if mute is True:
            utility.enable_print()
        return capacity, used_space, free_space


class GoogleDriveCloud:
    # TODO implement upload_folder, download_file, download_folder, delete and storage_status functions
    SCOPES = ['https://www.googleapis.com/auth/drive']
    CHUNK_SIZE = 4 * 1024 * 1024

    def __init__(self, credentials: str):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        path = credentials.rsplit("/", 1)[0]
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(path + '/token.pickle'):
            with open(path + '/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            if os.path.exists(path + '/token.pickle'):
                os.remove(path + '/token.pickle')
            with open(path + '/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                os.system("attrib +h {0}/token.pickle".format(path))

        service = build('drive', 'v3', credentials=creds)
        print("Successfully Initialized Google Drive API")

        self.drive_service = service
        self.folders_metadata = []

        results = self._drive_v3_api_()
        items = results.get('files', [])
        if items is not None:
            for item in items:
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    self.folders_metadata.append(item)

    def _drive_v3_api_(self):
        all_results = {}
        results = self.drive_service.files().list(pageSize=10,
                                                  fields="nextPageToken, files(name, mimeType, parents, id)").execute()
        all_results.update(results)
        while 'nextPageToken' in results:
            results = self.drive_service.files().list(
                pageToken=results['nextPageToken'], pageSize=10,
                fields="nextPageToken, files(name, mimeType, parents, id)").execute()
            all_results['files'].extend(results['files'])
        return all_results

    def _create_folder_(self, name, path="/"):
        try:
            next(item for item in self.folders_metadata if item['name'] == name)
        except StopIteration:
            folder_metadata = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
            if path != "/":
                head, mother_folder = ntpath.split(path)
                mother_folder_id = (next(item for item in self.folders_metadata if item['name'] == mother_folder))['id']
                folder_metadata.update({'parents': [mother_folder_id]})
            folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
            folder_metadata.update(folder)
            self.folders_metadata.append(folder_metadata)
            return
        raise NameError('The name "{0}" is already used by another folder'.format(name))

    def get_files_metadata(self, path=None):
        files_list = []
        results = self._drive_v3_api_()
        items = results.get('files', [])
        if not items:
            print("No items found")
        else:
            if path is None:
                for item in items:
                    files_list.append([item['name'], item['id'], item['parents']])
            else:
                head, mother_folder = ntpath.split(path[:-1])
                try:
                    mother_folder_id = \
                        (next(item for item in self.folders_metadata if item['name'] == mother_folder))['id']
                except StopIteration:
                    raise NotADirectoryError("The %s path does not exist" % path)
                for item in items:
                    if item['parents'] == [mother_folder_id]:
                        files_list.append([item['name'], item['id'], item['parents']])
        return files_list

    def get_files_names(self, path=None):
        metadata = self.get_files_metadata(path + "/")
        remote_files = {}
        for file in metadata:
            remote_path, _ = ntpath.split(self.get_file_path(file[0], file[2]))
            if remote_path not in remote_files.keys():
                remote_files.update({remote_path: [file[0]]})
            else:
                remote_files[remote_path].append(file[0])
        return remote_files

    def get_file_path(self, file_name, parent_id=None):
        tree = []
        if parent_id:
            while True:
                folder = self.drive_service.files().get(fileId=parent_id[0], fields='id, name, parents').execute()
                parent_id = folder.get('parents')
                if parent_id is None:
                    break
                tree.append({'id': parent_id[0], 'name': folder.get('name')})

        path = ''
        for i in range(len(tree)-1, -1, -1):
            path = path + tree[i]['name'] + "/"
        path = path + file_name
        return path

    def upload_file(self, directory, session: bool, path=""):
        head, tail = ntpath.split(directory)
        name, extension = tail.split('.')
        if session:
            media = MediaFileUpload(directory, mimetype='{0}/{1}'.format(name, extension), resumable=True,
                                    chunksize=self.CHUNK_SIZE)
            if path == "":
                file_metadata = {'name': tail}
                file = self.drive_service.files().create(body=file_metadata, media_body=media).execute()
                print('File ID %s' % file.get('id'))
            else:
                head, mother_folder = ntpath.split(path)
                try:
                    mother_folder_id = \
                        (next(item for item in self.folders_metadata if item['name'] == mother_folder))['id']
                except StopIteration:
                    raise NotADirectoryError("The %s directory does not exist" % directory)
                file_metadata = {'name': tail, 'parents': [mother_folder_id]}
                file = self.drive_service.files().create(body=file_metadata, media_body=media).execute()
                print('File ID %s' % file.get('id'))
        # ==================================================
        else:
            media = MediaFileUpload(directory, mimetype='{0}/{1}'.format(name, extension))
            if path is None:
                file_metadata = {'name': tail}
                file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print('File ID %s' % file.get('id'))
            else:
                head, mother_folder = ntpath.split(path)
                try:
                    mother_folder_id = \
                        (next(item for item in self.folders_metadata if item['name'] == mother_folder))['id']
                except StopIteration:
                    raise NotADirectoryError("The %s directory does not exist" % directory)
                file_metadata = {'name': tail, 'parents': [mother_folder_id]}
                file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                print('File ID %s' % file.get('id'))

    def upload_folder(self, directory, path="/"):
        __count__ = len(directory.split('/')) - 2
        self._create_folder_(directory.split('/')[__count__], '/' + path[:-1])
        path = path + directory.split('/')[__count__]
        for filename in os.listdir(directory):
            file_directory = directory + filename + '/'
            if os.path.isfile(file_directory[:-1]):
                file_directory = file_directory[:-1]
                file_size = convert.convert_bytes_to_mb(os.stat(file_directory).st_size)[0]
                if file_size < 100:
                    self.upload_file(file_directory, False, path)
                else:
                    self.upload_file(file_directory, True, path)
            elif os.path.isdir(file_directory):
                self.upload_folder(file_directory, directory)

    def download_file(self, path, directory):
        head, tail = ntpath.split(path)
        if head != '':
            files = self.get_files_metadata(head + '/')
        else:
            files = self.get_files_metadata()
        mother_folder = ntpath.split(head)[len(ntpath.split(head))-1]
        try:
            mother_folder_id = (next(item for item in self.folders_metadata if item['name'] == mother_folder))['id']
        except StopIteration:
            raise NotADirectoryError("The %s path does not exist" % path)
        file_id = None
        for file in files:
            if tail == file[0] and [mother_folder_id] == file[2]:
                file_id = file[1]
                break
        media = self.drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, media, self.CHUNK_SIZE)

        progress_bar = ttk.Progressbar(orient='horizontal', length=286, mode='determinate')
        progress_bar.grid(column=0, row=1, pady=10)
        progress_bar['maximum'] = 100
        progress_bar.start()
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            progress_bar['value'] = int(status.progress() * 100)
            progress_bar.update()
            print("Downloaded: %d%%." % int(status.progress()*100))
        print("Download completed")
        with open(directory + tail, 'wb') as out:
            fh.seek(0)
            out.write(fh.read())

    def download_folder(self):
        pass

    def delete_file(self):
        pass

    def delete_folder(self):
        pass

    def storage_status(self):
        pass


class MegaUploadCloud:
    MEGA_BASH_DIRECTORY = MEGA_BASH_DIR + "\\"

    def __init__(self, email, password):
        subprocess.call(self.MEGA_BASH_DIRECTORY + 'mega-logout.bat', stdout=subprocess.DEVNULL)
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-login.bat', email, password]
        status = subprocess.call(cmd_line, stdout=subprocess.DEVNULL)
        if status == 0:
            print("Successfully Initialized Mega Upload API")
        elif status == 9:
            raise e.LoginError("Invalid email or password")
        elif status == 1:
            raise e.ServerError("Failed to access server")
        else:
            raise Exception("An unknown error occurred while trying to log in, error status: {0}".format(status))

    def _create_folder_(self, name, path=None):
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-cd.bat']
        if path is not None:
            cmd_line.append(path)
        subprocess.call(cmd_line)
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-mkdir.bat', name]
        status = subprocess.call(cmd_line)
        if status == 0:
            return
        elif status == 54:
            raise IsADirectoryError('The name "{0}" is already used by another folder'.format(name))

    def get_files_names(self, path=None, mute=True):
        if mute:
            utility.block_print()
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-ls.bat']
        if path is not None:
            cmd_line.append(path)
        files = subprocess.getoutput(cmd_line)
        print(files)
        utility.enable_print()
        files = files.split('\n')
        return files

    def get_all_subdirs_files_names(self, path, service=None, remote_files={}):
        temp = self.get_files_names(path)
        remote_files.update({path: temp})
        for file in temp:
            if len(file.split('.')) == 1:
                path = (os.path.join(path, file)).replace("\\", '/')
                self.get_all_subdirs_files_names(path, service, remote_files)
        return remote_files

    def upload(self, local_path, remote_path=None):
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-put.bat', local_path]
        if remote_path is not None:
            remote_path = remote_path.replace('\\', "/")
            cmd_line.append(remote_path)
        status = subprocess.call(cmd_line)
        if status == 0:
            print("Upload Completed")
        elif status == 53:
            raise NotADirectoryError('The directory "{0}" does not exist'.format(local_path))

    def download(self, remote_path, local_path):
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-get.bat', remote_path, local_path]
        status = subprocess.call(cmd_line)
        if status == 0:
            return
        elif status == 53:
            raise NotADirectoryError('The MEGA path "{0}" does not exist'.format(remote_path))

    def delete(self, path):
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-rm.bat', path]
        status = subprocess.call(cmd_line)
        if status == 0:
            return
        elif status == 53:
            raise NotADirectoryError('The MEGA path "{0}" does not exist'.format(path))

    def storage_status(self):
        cmd_line = [self.MEGA_BASH_DIRECTORY + 'mega-du.bat']
        used_space_bytes = subprocess.getoutput(cmd_line)
        used_space_bytes = int(used_space_bytes.split(':')[2])
        gb, mb = convert.convert_bytes_to_gb(used_space_bytes)
        used_space = {"GB": gb, "MB": mb}