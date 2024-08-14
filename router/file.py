from fastapi import APIRouter, File, UploadFile, Query
import shutil
import os
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/file",
    tags=["file"],
    responses={404: {"description": "Not found"}}
)

@router.post("/file/")
def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    lines = [line.strip() for line in lines]
    return {"lines": lines}

@router.post("/uploadfile/")
def get_uploadfile(upload_file: UploadFile = File(...)):
    path = f"files/{upload_file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {
        "filename": path,
        "type": upload_file.content_type}

@router.get("/download/{name}/", response_class=FileResponse)
def get_file(name: str):
    path = f"files/{name}"
    return path

def get_files():
    files = os.listdir("files")
    return files

available_files = get_files()

@router.get("/download/", response_class=FileResponse)
def download_file(file_name: str = 
                  Query(..., description="Selecciona un archivo",
                        enum=available_files)):
    file_path = f"./files/{file_name}"
    return file_path
