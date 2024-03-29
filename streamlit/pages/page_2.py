import streamlit as st
from menu import menu
import re
import boto3
import os
from service import trigger_airflow_pipeline

from dotenv import dotenv_values

# Load environment variables
config = dotenv_values(".env")

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=config["S3_ACCESS_KEY"],
    aws_secret_access_key= config["S3_SECRET_KEY"],
    region_name= config["S3_REGION"] 
)

def list_pdf_files(bucket_name, folder_name):
    """List PDF files in a specific S3 bucket folder."""
    pdf_files = []
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=folder_name):
        for obj in page.get('Contents', []):
            if obj['Key'].lower().endswith('.pdf'):
                pdf_files.append(obj['Key'])
    return pdf_files



def is_valid_s3_path(path):
    """
    Check if the entered path is a valid S3 path.
    Valid S3 path format: s3://bucket_name/path/to/file
    """
    pattern = r"s3://([a-zA-Z0-9.-]+)/(.+)"
    return re.match(pattern, path) is not None



menu()
st.title("Trigger Airflow")


# Define your bucket and folder name
bucket_name = st.text_input('Enter S3 Bucket Name:', 'cfa-pdfs')
folder_name = st.text_input('Enter Folder Name:', 'uploads')

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object."""
    return s3_client.generate_presigned_url('get_object',
                                            Params={'Bucket': bucket_name,
                                                    'Key': object_name},
                                            ExpiresIn=expiration)

if st.button('List PDF Files'):
        if bucket_name and folder_name:
            try:
                pdf_files = list_pdf_files(bucket_name, folder_name)
                if pdf_files:
                    for file in pdf_files:
                        file_url = generate_presigned_url(bucket_name, file)
                        st.markdown(f"📄 [{file.split('/')[-1]}]({file_url})")
                else:
                    st.write("No PDF files found in the specified folder.")
            except Exception as e:
                st.error(f"Error accessing S3 Bucket: {e}")
        else:
            st.warning("Please enter both the S3 Bucket Name and Folder Name.")



st.title('Trigger Airflow DAG')

# Creating text input for each required field
host = st.text_input('Host', "http://airflow-webserver:8080")
dag_id = st.text_input('DAG ID', "sandbox")
username = st.text_input('Username', "airflow")
password = st.text_input('Password', type='password')  # Masking the password input

# Button to trigger the pipeline
if st.button('Trigger Pipeline'):
    result = trigger_airflow_pipeline(host, dag_id, username, password)
    print(result)
    # Check the result and display a message
    if result == "Success":
        st.markdown("<h2 style='color: green;'>Success</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color: red;'>Failure</h2>", unsafe_allow_html=True)








