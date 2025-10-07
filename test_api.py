"""
Script de prueba para validar el funcionamiento básico de la API
"""
import requests
import json
import os
from pathlib import Path

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Iniciando pruebas de la API...")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Servidor respondiendo correctamente")
        else:
            print("❌ Servidor no responde")
            return
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        print("💡 Ejecuta: python main.py")
        return
    
    # Probar endpoint raíz
    response = requests.get(f"{base_url}/")
    if response.status_code == 200:
        print("✅ Endpoint raíz funcionando")
        print(f"📝 Respuesta: {response.json()}")
    
    # Probar listar archivos (carpetas vacías)
    for folder in ["documents", "ocr", "embeddings"]:
        response = requests.get(f"{base_url}/{folder}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Listado de {folder}: {data['count']} archivos")
    
    # Crear archivos de prueba
    test_files = {
        "documents": ("test.pdf", b"Contenido PDF simulado"),
        "ocr": ("test_ocr.json", json.dumps({"text": "Texto extraído"}).encode()),
        "embeddings": ("test_embeddings.json", json.dumps({"vector": [0.1, 0.2, 0.3]}).encode())
    }
    
    print("\n📤 Probando subida de archivos...")
    
    for folder, (filename, content) in test_files.items():
        files = {"file": (filename, content)}
        response = requests.post(f"{base_url}/{folder}/", files=files)
        
        if response.status_code == 200:
            print(f"✅ Archivo {filename} subido a {folder}")
        else:
            print(f"❌ Error subiendo {filename}: {response.status_code} - {response.text}")
    
    print("\n📥 Probando descarga de archivos...")
    
    for folder, (filename, _) in test_files.items():
        response = requests.get(f"{base_url}/{folder}/{filename}")
        
        if response.status_code == 200:
            print(f"✅ Archivo {filename} descargado de {folder}")
        else:
            print(f"❌ Error descargando {filename}: {response.status_code}")
    
    print("\n🔄 Probando listado con archivos...")
    
    for folder in ["documents", "ocr", "embeddings"]:
        response = requests.get(f"{base_url}/{folder}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {folder}: {data['count']} archivos encontrados")

if __name__ == "__main__":
    test_api()