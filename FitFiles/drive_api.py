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
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
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

def list_files(service, parent_id, time_threshold):
    query = f"'{parent_id}' in parents and mimeType!='application/vnd.google-apps.folder' and modifiedTime > '{time_threshold.isoformat()}Z'"
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

def update_workout_database(service, db):
    # Get the Workout_Data folder ID
    workout_data_id = get_folder_id(service, 'Workout_Data')
    if not workout_data_id:
        print("Workout_Data folder not found")
        return

    # Set time threshold (e.g., 24 hours ago)
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    # List athlete folders
    athlete_folders = list_folders(service, workout_data_id)

    for athlete_folder in athlete_folders:
        athlete_id = athlete_folder['name']
        
        # List workout type folders
        workout_type_folders = list_folders(service, athlete_folder['id'])
        
        for workout_type_folder in workout_type_folders:
            workout_type = workout_type_folder['name']
            
            # List new files in the workout type folder
            new_files = list_files(service, workout_type_folder['id'], time_threshold)
            
            for file in new_files:
                # Download the file
                local_file_path = download_file(service, file['id'], file['name'])
                
                # Add the workout to the database
                db.add_workout(athlete_id, workout_type, local_file_path)
                
                # Optionally, delete the local file after adding to the database
                os.remove(local_file_path)

    print("Workout database updated successfully")

# Usage example
if __name__ == '__main__':
    service = get_drive_service()  # Assuming you have this function from previous setup
    db = WorkoutDatabase()  # Initialize your database
    update_workout_database(service, db)