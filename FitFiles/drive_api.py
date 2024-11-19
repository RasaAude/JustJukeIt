from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
from workout_database import WorkoutDatabase
from googleapiclient.http import MediaIoBaseDownload
import io
import os
from datetime import datetime, timedelta
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def list_files(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

def get_folder_id(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields="files(id)").execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

def list_folders(service, parent_id):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def list_files(service, parent_id):
    query = f"'{parent_id}' in parents and mimeType!='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.seek(0)
    with open(file_name, 'wb') as f:
        f.write(fh.read())
    return file_name

def create_workout_folder(service, folder_name):
    # Get the Workout_Data folder ID
    workout_data_id = get_folder_id(service, 'Workout_Data')
    if not workout_data_id:
        print("Workout_Data folder not found")
        return None
    # Check if the folder already exists
    if check_folder_exists(service, workout_data_id, folder_name):
        print(f"Folder '{folder_name}' already exists in Workout_Data.")
        return None
    
    # Create the new folder
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [workout_data_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    new_folder_id = folder.get('id')

    # List of sub-folders to create
    sub_folders = ['40_Min', '20_Min', '5_Min', '3_Min', '10_Min' '2K', '6K']

    # Create sub-folders
    for sub_folder in sub_folders:
        sub_folder_metadata = {
            'name': sub_folder,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [new_folder_id]
        }
        service.files().create(body=sub_folder_metadata).execute()

    print(f"Created folder '{folder_name}' with sub-folders in Workout_Data")
    return new_folder_id

def add_folder_to_all_subfolders(service, new_folder_name):
    # Get the Workout_Data folder ID
    workout_data_id = get_folder_id(service, 'Workout_Data')
    if not workout_data_id:
        print("Workout_Data folder not found")
        return

    # Query to get all subfolders of Workout_Data
    query = f"'{workout_data_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    subfolders = results.get('files', [])

    for subfolder in subfolders:
        subfolder_id = subfolder['id']
        subfolder_name = subfolder['name']
        
        # Create new folder in each subfolder
        new_folder_metadata = {
            'name': new_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [subfolder_id]
        }
        
        print(f"Created folder '{new_folder_name}' in subfolder '{subfolder_name}'")

    print(f"Added '{new_folder_name}' to all subfolders in Workout_Data")

def check_folder_exists(service, parent_folder_id, folder_name):
    query = "mimeType='application/vnd.google-apps.folder' and name='{}' and '{}' in parents".format(folder_name, parent_folder_id)
    results = service.files().list(q=query, fields='files(id, name)').execute()
    return len(results.get('files', [])) > 0

def update_workout_database(service, db):
    workout_data_id = get_folder_id(service, 'Workout_Data')
    if not workout_data_id:
        print("Workout_Data folder not found")
        return

    athlete_folders = list_folders(service, workout_data_id)

    for athlete_folder in athlete_folders:
        athlete_id = athlete_folder['name']
        workout_type_folders = list_folders(service, athlete_folder['id'])

        for workout_type_folder in workout_type_folders:
            workout_type = workout_type_folder['name']
            all_files = list_files(service, workout_type_folder['id'])

            for file in all_files:
                local_file_path = download_file(service, file['id'], file['name'])
                #print(f"Adding {athlete_id}'s {workout_type} with file path {local_file_path}")
                db.add_workout(athlete_id, workout_type, local_file_path)

                # Delete the local file immediately after adding to the database
                try:
                    os.remove(local_file_path)
                    #print(f"Deleted local file: {local_file_path}")
                except Exception as e:
                    print("")#f"Error deleting {local_file_path}: {str(e)}")

    print("Workout database updated successfully")

def share_athlete_folders(service):
    workout_data_id = get_folder_id(service, 'Workout_Data')
    if not workout_data_id:
        print("Workout_Data folder not found")
        return

    # List all athlete folders within Workout_Data
    athlete_folders = list_folders(service, workout_data_id)

    for athlete_folder in athlete_folders:
        athlete_id = athlete_folder['name']
        athlete_folder_id = athlete_folder['id']
        athlete_email = f"{athlete_id}@columbia.edu"

        # Set up the permission
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': athlete_email
        }

        try:
            # Share the folder with the athlete
            service.permissions().create(
                fileId=athlete_folder_id,
                body=user_permission,
                sendNotificationEmail=True
            ).execute()
            print(f"Shared folder for athlete {athlete_id} with {athlete_email}")
        except Exception as e:
            print(f"Error sharing folder for athlete {athlete_id}: {str(e)}")