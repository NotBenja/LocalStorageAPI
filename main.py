from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
from pathlib import Path
from typing import List

app = FastAPI(
    title="Cloud Storage API",
    description="Una API simple que simula el comportamiento de Cloud Storage con 3 carpetas: documents, ocr y embeddings",
    version="1.0.0"
)

# Directorio base para el storage
STORAGE_BASE = Path("storage")
FOLDERS = ["documents", "ocr", "embeddings"]

# Crear carpetas si no existen
for folder in FOLDERS:
    (STORAGE_BASE / folder).mkdir(parents=True, exist_ok=True)

# Tipos de archivo permitidos por carpeta
ALLOWED_TYPES = {
    "documents": [".pdf"],
    "ocr": [".json"],
    "embeddings": [".json", ".npy", ".pkl"]  # Agregué algunos formatos comunes para embeddings
}

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Cloud Storage API",
        "version": "1.0.0",
        "folders": FOLDERS,
        "endpoints": {
            "GET": "/{folder}/{filename} - Obtener un archivo",
            "POST": "/{folder}/ - Subir un archivo"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

def validate_folder(folder: str):
    """Valida que la carpeta sea una de las permitidas"""
    if folder not in FOLDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Folder '{folder}' no es válida. Carpetas permitidas: {FOLDERS}"
        )

def validate_file_type(folder: str, filename: str):
    """Valida que el tipo de archivo sea permitido para la carpeta"""
    file_extension = Path(filename).suffix.lower()
    allowed_extensions = ALLOWED_TYPES.get(folder, [])
    
    if allowed_extensions and file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo '{file_extension}' no permitido en '{folder}'. Tipos permitidos: {allowed_extensions}"
        )

@app.get("/{folder}/{filename}")
async def get_file(folder: str, filename: str):
    """
    Obtener un archivo de una carpeta específica
    
    - **folder**: Nombre de la carpeta (documents, ocr, embeddings)
    - **filename**: Nombre del archivo a obtener
    """
    validate_folder(folder)
    
    file_path = STORAGE_BASE / folder / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Archivo '{filename}' no encontrado en la carpeta '{folder}'"
        )
    
    if not file_path.is_file():
        raise HTTPException(
            status_code=400,
            detail=f"'{filename}' no es un archivo válido"
        )
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )

@app.post("/{folder}/")
async def upload_file(folder: str, file: UploadFile = File(...)):
    """
    Subir un archivo a una carpeta específica
    
    - **folder**: Nombre de la carpeta (documents, ocr, embeddings)
    - **file**: Archivo a subir
    """
    validate_folder(folder)
    validate_file_type(folder, file.filename)
    
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="El archivo debe tener un nombre válido"
        )
    
    file_path = STORAGE_BASE / folder / file.filename
    
    # Verificar si el archivo ya existe
    if file_path.exists():
        raise HTTPException(
            status_code=409,
            detail=f"El archivo '{file.filename}' ya existe en la carpeta '{folder}'"
        )
    
    try:
        # Guardar el archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": f"Archivo '{file.filename}' subido exitosamente a '{folder}'",
            "filename": file.filename,
            "folder": folder,
            "size": file_path.stat().st_size
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar el archivo: {str(e)}"
        )

@app.get("/{folder}/")
async def list_files(folder: str):
    """
    Listar todos los archivos en una carpeta específica
    
    - **folder**: Nombre de la carpeta (documents, ocr, embeddings)
    """
    validate_folder(folder)
    
    folder_path = STORAGE_BASE / folder
    
    try:
        files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime
                })
        
        return {
            "folder": folder,
            "files": files,
            "count": len(files)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al listar archivos: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)