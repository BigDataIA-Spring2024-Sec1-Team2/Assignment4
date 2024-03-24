from fastapi import APIRouter, HTTPException, Response
from dotenv import dotenv_values
from fastapi import FastAPI, File, UploadFile
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging
from utils.util import generate_file_name, is_pdf

router = APIRouter()

config = dotenv_values(".env")

# Create an S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=config["S3_ACCESS_KEY"],
    aws_secret_access_key=config["S3_SECRET_KEY"],
    region_name=config["S3_REGION"]
)

@router.post("/upload_s3/")
async def upload_file(file_obj: UploadFile = File(...)):
    if not is_pdf(file_obj.filename):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        # Upload the file to S3
        S3_BUCKET_NAME = config["S3_BUCKET_NAME"]
        folder_name = config["S3_UPLOAD_PDF_FOLDER"]
        file_name = generate_file_name()
        print("filename = ", file_name)
        success = upload_file_to_bucket(file_obj.file, S3_BUCKET_NAME,folder_name, file_name)
        print("Uploaded ", file_name, " to S3 bucket")
        if success:
            print("Uploaded ", file_name, " to S3 bucket")
            s3_link = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{folder_name}/{file_name}"
            print("s3_link to access the file", s3_link)
            return {"status": "Success", "message": "File uploaded successfully", "s3_link": s3_link}
        else:
            return {"status": "Failure", "error": "Some error occurred"}
    except NoCredentialsError:
        return {"status": "Failure", "error": "AWS credentials not found or invalid"}
    except Exception as e:
        print(str(e))
        return {"status": "Failure", "error": "Something went wrong"}

def upload_file_to_bucket( file_obj, bucket, folder, object_name=None):
    """Upload a file to an S3 bucket

    :param file_obj: File to upload
    :param bucket: Bucket to upload to
    :param folder: Folder to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_obj

    # Upload the file
    try:
        s3_client.upload_fileobj(file_obj, bucket, f"{folder}/{object_name}")
    except ClientError as e:
        logging.error(e)
        return False
    except NoCredentialsError:
        logging.error(e)
        return False
    except Exception as e:
        logging.error(e)
        return False
    return True
