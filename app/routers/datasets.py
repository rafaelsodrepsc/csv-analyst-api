from fastapi import APIRouter, UploadFile
from services import dataService

router = APIRouter()

@router.post("/uploadfile")
async def upload_file(file: UploadFile):
    content = await file.read()
    return dataService.process_upload(file.filename,content)