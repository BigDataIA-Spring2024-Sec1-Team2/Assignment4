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

# Function to perform Airflow health check
def check_airflow_health(airflow_url):
    try:
        response = requests.get(f"{airflow_url}/health")
        if response.status_code == 200:
            data = response.json()
            # Creating a summary of the health status for each component
            statuses = []
            for component, details in data.items():
                status = details['status']
                if status is None:
                    status = 'No status'
                statuses.append(f"{component}: {status}")
            # Joining all statuses into a single string for display
            return '\n'.join(statuses)
        else:
            return "Airflow server returned an error."
    except Exception as e:
        return str(e)
