from fastapi import FastAPI
from routers import airflow_service
from routers import aws_service

app = FastAPI()
app.include_router(airflow_service.router)
app.include_router(aws_service.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
