import io
import csv
import os
import threading
import time
import signal
import sys
import pandas as pd
import json
from googleapiclient.http import MediaIoBaseDownload
from Google import create_service
from pymongo import MongoClient
from datetime import datetime, timedelta

n = 0
count = 0
runflag = True
folder_id = '148H9UolW5UpJIv5HTIqQSPdBpdrpUI22'  # GoogleDrive Folder id
base_date = '2022_09_01'    # Base date from where to start
file_name = 'raw_'+base_date+'.csv'
previous_file_name = ''
print(f"Current file name is : {file_name}")
directory = "DriveData"
CLIENT_SECRET_FILE = 'Client_Secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def get_updated_files_list():
    """Gets the latest list of files from the GoogleDrive folder"""
    global folder_id, service

    folder_id = '148H9UolW5UpJIv5HTIqQSPdBpdrpUI22'     # GoogleDrive Folder ID
    query = f"parents = '{folder_id}'"

    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    df = pd.DataFrame(files)
    return df


def signal_handling(signum, frame):
    print("Exiting ...")
    global runflag
    runflag = False
    sys.exit()


signal.signal(signal.SIGINT, signal_handling)

def create_dir():
    path = os.path.abspath(directory)
    # Make a directory in the base folder to store the downloaded files from the GoogleDrive
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

class MongoDBClient:
    def __init__(
        self,
        db: str
    ) -> None:
        self.client = MongoClient('mongodb://mongodb:27017')
        self.db = self.client[db]


def timer() -> None:
    """timer() increments one day in the filename per every 5 min
    which gives us the new filename to be downloaded from the GoogleDrive"""
    print("Timer Started...")
    global base_date, file_name, runflag, n, count
    try:
        while runflag:
            # put this in a thread which runs for every 5 min
            new_date = (datetime.strptime(base_date, '%Y_%m_%d') + timedelta(days=n)).strftime('%Y_%m_%d')
            base_date = new_date
            file_name = 'raw_' + new_date + '.csv'
            print(f"New filename is : {file_name}")
            downloader(filename=file_name)
            count += 1
            if count > 0:
                n = 1
            time.sleep(1)       # Time interval at which new file needs to be downloaded
    except Exception as exception:
        print(exception)
    print("Timer function ended")

def downloader(filename) -> None:
    """downloader() downloads new file if there is a change in the filename
    :param filename: Name of the file which needs to be downloaded form GoogleDrive"""
    global MONGO_CLIENT
    files = get_updated_files_list()
    df1 = files['name'] == file_name
    if df1.values.sum():
        dfb = files[df1].index.values.astype(int)[0]
        file_id = files['id'][dfb]
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloading = MediaIoBaseDownload(fd=fh, request=request)

        done = False

        while not done:
            status, done = downloading.next_chunk()
            print("Downloaded Progress {0}".format(status.progress()*100))

        fh.seek(0)

        with open(os.path.join('./DriveData', file_name), 'wb') as f:
            f.write(fh.read())
        f.close()
        data = pd.read_csv(os.path.join('./DriveData', file_name))
        formated_data = json.loads(data.to_json(orient='records'))
        print(MONGO_CLIENT.db.sessions.find_one({
            'session_id': 'a97ff060-462e-432d-a120-610d1440f068',
        }))
        MONGO_CLIENT.db.sessions.insert_many(list(formated_data))
    else:
        print(f"There is no {file_name} file in the GoogleDrive Folder ID {folder_id}")


if __name__ == "__main__":
    create_dir()    # Create a directory to store the downloaded files
    MONGO_CLIENT = MongoDBClient('clients')

    print("Synchronization Service Started ...")

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()
    timer_thread.join()
