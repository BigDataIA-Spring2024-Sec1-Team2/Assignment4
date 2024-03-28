from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Paths(BaseModel):
    input_path: str
    output_path: str

@app.post("/process-pdf/")
def process_pdf_with_grobid(paths: Paths):
    # Construct the URL for the Grobid service
    grobid_url = "http://localhost:8070/api/processFulltextDocument"
    
    # Open the input file in binary mode and send it to Grobid
    try:
        with open(paths.input_path, "rb") as file:
            response = requests.post(grobid_url, files={"input": file})
        
        # Check if Grobid processed the file successfully
        if response.status_code == 200:
            # Write the Grobid response content to the specified output path
            with open(paths.output_path, "wb") as f:
                f.write(response.content)
            return {"message": "File processed successfully"}
        else:
            return HTTPException(status_code=500, detail="Grobid processing failed")
    except Exception as e:
        # Handle errors, such as file not found
        return HTTPException(status_code=500, detail=str(e))
