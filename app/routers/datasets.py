from fastapi import APIRouter, UploadFile
from services import dataService

router = APIRouter()

@router.post("/uploadfile")
async def upload_file(file: UploadFile):
    content = await file.read()
    return dataService.process_upload(file.filename,content)

@router.get('/view_dataset')
async def view_file():
    return dataService.list_datasets()

@router.get('/datasets/{id}')
async def get_dataset(id : str):
    return dataService.get_dataset(id)

@router.get('/datasets/{id}/preview')
async def preview_dataset(id: str, rows: int = 5):
    return dataService.preview_dataset(id, rows)
