import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    filename = 'token_download.pickle'
    if os.path.exists(filename):
        with open(filename, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(filename, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def create_folder_upload_files(filename,folder_name=None,folder_id=None,upload_name=None):
    """
    Creates a folder  and upload a file to it
    """
    
    #Checking Stuffs
    if folder_name and folder_id:
        print("Please provide only on of the following...")
        print("""
1. Folder name : If you want to create a folder, Just give its name.
2. Folder id : If you want to add file into existing folder, just give its id
3. Neither folder name nor folder id: Add file to root of the drive.
""")
    
    
    # authenticate account
    service = get_gdrive_service()
    media = MediaFileUpload(filename, resumable=True)
    
    
    
    if folder_name:
        # folder details we want to make
        folder_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        # create the folder
        file = service.files().create(body=folder_metadata, fields="id").execute()
        # get the folder id
        folder_id = file.get("id")
        print("New Folder ID: %s \n" % folder_id)
    if not upload_name:
        upload_name = filename
    if folder_id:
        # upload a file text file
        # first, define file metadata, such as the name and the parent folder ID
        file_metadata = {
            "name": upload_name,
            "parents": [folder_id]
        }
    else:
        # upload a file text file
        # first, define file metadata, such as the name
        file_metadata = {
            "name": upload_name
        }

    # upload
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File uploaded, id:", file.get("id"))
        

def update_upload_file(filename,file_id,rename = None):
    """
    Replace file of file id present in drive with filename.
    """
    service = get_gdrive_service()
    media = MediaFileUpload(filename, resumable=True)
    body = {}
    if rename:
        if rename == True:
            rename = filename
        body['name'] = rename
    file = service.files().update(
        fileId = file_id,
        body = body,
        media_body=media
    ).execute()
    print("File updated, id:", file.get("id"))

if __name__ == '__main__':
    create_folder_upload_files(filename = "sd.md",folder_name="MD Files")
    # update_upload_file(filename = "test.txt", file_id = "1NKt8OYlaQhMmzUaZvqsg3uwRtUHGfYe3", rename="Db.txt")
    