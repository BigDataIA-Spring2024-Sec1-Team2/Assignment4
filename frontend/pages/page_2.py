import streamlit as st
from menu import menu
import re

def is_valid_s3_path(path):
    """
    Check if the entered path is a valid S3 path.
    Valid S3 path format: s3://bucket_name/path/to/file
    """
    pattern = r"s3://([a-zA-Z0-9.-]+)/(.+)"
    return re.match(pattern, path) is not None


menu()
st.title("Trigger Airflow")
# Input field for S3 file path
s3_file_path = st.text_input("Enter S3 File Path of the PDF")

if st.button("Submit"):
    if s3_file_path:
        if is_valid_s3_path(s3_file_path):
            st.write("S3 File Path submitted:", s3_file_path)
        else:
            st.write("Invalid S3 file path. Please enter a valid path in the format: s3://bucket_name/path/to/file")
    else:
        st.write("Please enter a valid S3 file path")


