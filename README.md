# Cloud Storage API

Una API simple que simula el comportamiento de Cloud Storage con 3 carpetas específicas: `documents`, `ocr` y `embeddings`.

## Estructura del Proyecto

```
LocalStorageAPI/
├── main.py              # Aplicación FastAPI principal
├── requirements.txt     # Dependencias Python
├── storage/            # Directorio de almacenamiento
│   ├── documents/      # Archivos PDF
│   ├── ocr/           # Archivos JSON (resultados OCR)
│   └── embeddings/    # Archivos JSON, NPY, PKL (embeddings)
└── README.md          # Este archivo
```

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv .venv
```

2. Activar el entorno virtual:
```bash
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la API:

```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

## Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Documentación interactiva (Swagger UI)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## Endpoints

### Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información general de la API |
| GET | `/health` | Health check |
| GET | `/{folder}/` | Listar archivos en una carpeta |
| GET | `/{folder}/{filename}` | Descargar un archivo específico |
| POST | `/{folder}/` | Subir un archivo a una carpeta |

### Carpetas disponibles

- **documents**: Solo archivos PDF (`.pdf`)
- **ocr**: Solo archivos JSON (`.json`)
- **embeddings**: Archivos JSON, NPY, PKL (`.json`, `.npy`, `.pkl`)

## Ejemplos de uso

### 1. Subir un archivo PDF a documents

```bash
curl -X POST "http://localhost:8000/documents/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@documento.pdf"
```

### 2. Obtener un archivo

```bash
curl -X GET "http://localhost:8000/documents/documento.pdf" \
     --output documento_descargado.pdf
```

### 3. Listar archivos en una carpeta

```bash
curl -X GET "http://localhost:8000/documents/"
```

### 4. Subir resultado OCR

```bash
curl -X POST "http://localhost:8000/ocr/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@resultado_ocr.json"
```

### 5. Subir embeddings

```bash
curl -X POST "http://localhost:8000/embeddings/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@embeddings.json"
```

## Validaciones

- ✅ Solo se permiten las carpetas: `documents`, `ocr`, `embeddings`
- ✅ Validación de tipos de archivo por carpeta
- ✅ No se permite sobrescribir archivos existentes
- ✅ Manejo de errores comprehensivo
- ✅ Validación de nombres de archivo

## Códigos de respuesta

- **200**: Operación exitosa
- **400**: Error de validación (carpeta inválida, tipo de archivo no permitido)
- **404**: Archivo no encontrado
- **409**: Archivo ya existe
- **500**: Error interno del servidor

## Desarrollo

Para desarrollo con recarga automática:

```bash
uvicorn main:app --reload
```

## Estructura de respuestas

### Subir archivo exitoso
```json
{
  "message": "Archivo 'documento.pdf' subido exitosamente a 'documents'",
  "filename": "documento.pdf",
  "folder": "documents",
  "size": 1024
}
```

### Listar archivos
```json
{
  "folder": "documents",
  "files": [
    {
      "filename": "documento.pdf",
      "size": 1024,
      "modified": 1699123456.789
    }
  ],
  "count": 1
}
```