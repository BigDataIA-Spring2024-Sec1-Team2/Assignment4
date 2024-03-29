import requests
from dotenv import dotenv_values
import json

config = dotenv_values(".env")

def upload_file_api(file):
    config = dotenv_values(".env")
    api_endpont = config["API_URL"] + config["S3_UPLOAD_ENDPOINT"]
    print(api_endpont)
    files = {'file_obj': file}
    response = requests.post(api_endpont, files=files)
    print()
    print(response.json())
    print()
    res = response.json()
    if res['status'] == 'Success':
        return res['message']
    return res['message']

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
