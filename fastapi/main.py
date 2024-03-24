from fastapi import FastAPI
from routers import service, aws_service

app = FastAPI()
app.include_router(service.router, prefix="/api")
app.include_router(aws_service.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
