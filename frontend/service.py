import requests
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

def upload_file_api(file):
    api_endpont = config["API_URL"] + config["S3_UPLOAD_ENDPOINT"]

    files = {'file_obj': file}
    response = requests.post(api_endpont, files=files)
    print(response.json())
    res = response.json()
    if res['status'] == 'Success':
        return res['s3_link']
    return res['error']
