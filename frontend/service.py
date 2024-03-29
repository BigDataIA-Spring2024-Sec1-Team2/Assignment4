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


def trigger_airflow_pipeline(host,dag_id,username,password):
    config = dotenv_values(".env")
    api_endpont = config["API_URL"] + '/trigger_airflow_pipeline/'
    print(api_endpont)
    
    payload = {
    "host": host,  # The host of your Airflow instance
    "dag_id": dag_id,   # The DAG ID you want to trigger
    "username": username,        # The username for Airflow authentication
    "password": password         # The password for Airflow authentication
    }
    response = requests.get(api_endpont, params=payload)
    if response.status_code == 200:
        return "Success"
    else:
        print(response.json())
        return "Error"