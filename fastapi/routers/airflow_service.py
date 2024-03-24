from fastapi import APIRouter
from dotenv import dotenv_values
import time
import logging

router = APIRouter()

config = dotenv_values(".env")

from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

AIRFLOW_API_URL = config["AIRFLOW_API_URL"]
AIRFLOW_USERNAME = config["AIRFLOW_USERNAME"]
AIRFLOW_PASSWORD = config["AIRFLOW_PASSWORD"]

@router.get("/trigger_airflow_pipeline/")
async def trigger_airflow_pipeline(s3_file_path):
    response = trigger_pipeline(s3_file_path)
    if response:
        return {"status": "Success", "message": "Airflow pipeline triggered successfully"}
    return {"status": "Failure", "error": "Something went wrong. Try again."}
    

def trigger_pipeline(s3_file_path):
    return True
    # try: 
    #     # Prepare headers for Basic Authentication
    #     headers = {'Content-Type': 'application/json'}
    #     auth = (AIRFLOW_USERNAME, AIRFLOW_PASSWORD)

    #     # Prepare data to trigger the DAG
    #     data = {
    #         "conf": {"s3_file_path": s3_file_path}  # Pass any additional parameters needed by your DAG
    #     }
    #     # Trigger the Airflow DAG
    #     response = requests.post(AIRFLOW_API_URL, headers=headers, json=data, auth=auth)
    #     logging.info(f"Airflow response: {response}")
    #     if response.status_code == 200:
    #         return True
    #     else:
    #         logging.error("Some error occurred")
    #         return False

    # except Exception as e:
    #     logging.error(str(e))
    #     return False




@router.get("/pipeline_status/")
async def get_pipeline_status():
    status = get_status()
    if status:
        return {"status": "Success", "message": "Airflow pipeline status retrieved successfully", "airflow_status": status}
    else:
        return {"status": "Failure", "error": "Something went wrong"}
    
    
def get_status():
    return "Running"
    # try:
    #     # Fetch the status of the last run of the Airflow DAG
    #     response = requests.get(AIRFLOW_API_URL)
    #     last_run_status = response.json()["dag_runs"][0]["state"]
    #     return last_run_status
    # except Exception as e:
    #     logging.error(str(e))
    #     return None



