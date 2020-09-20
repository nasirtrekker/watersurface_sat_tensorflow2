# from https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

# How to execute script
## python download_url.py -i 'file id' -d 'download destination'
import requests
import argparse

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)



parser = argparse.ArgumentParser()
parser.add_argument('-i', '--id', help = 'File identifier of the google drive shared file')
parser.add_argument('-d', '--download', help = 'Download destination')

args = parser.parse_args()
download_file_from_google_drive(args.id, args.download)