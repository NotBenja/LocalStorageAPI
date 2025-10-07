#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Cloud Storage API con diferentes opciones
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Función principal del script"""
    
    # Verificar que estemos en el directorio correcto
    if not Path("main.py").exists():
        print("❌ Error: No se encuentra main.py en el directorio actual")
        print("💡 Asegúrate de ejecutar este script desde el directorio del proyecto")
        sys.exit(1)
    
    # Determinar el comando Python
    if Path(".venv").exists():
        if os.name == 'nt':  # Windows
            python_cmd = ".venv/Scripts/python.exe"
        else:  # Linux/Mac
            python_cmd = ".venv/bin/python"
    else:
        python_cmd = "python"
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "dev":
            print("🚀 Iniciando servidor en modo desarrollo...")
            subprocess.run([python_cmd, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
        
        elif command == "test":
            print("🧪 Ejecutando pruebas...")
            subprocess.run([python_cmd, "test_api.py"])
        
        elif command == "install":
            print("📦 Instalando dependencias...")
            subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"])
        
        elif command == "help":
            show_help()
        
        else:
            print(f"❌ Comando '{command}' no reconocido")
            show_help()
    
    else:
        print("🚀 Iniciando servidor...")
        subprocess.run([python_cmd, "main.py"])

def show_help():
    """Mostrar ayuda de comandos"""
    print("""
🔧 Cloud Storage API - Script de ejecución

Uso: python run.py [comando]

Comandos disponibles:
  (ninguno)  Ejecutar servidor en modo producción
  dev        Ejecutar servidor en modo desarrollo (auto-reload)
  test       Ejecutar pruebas de la API
  install    Instalar dependencias
  help       Mostrar esta ayuda

Ejemplos:
  python run.py          # Servidor en modo producción
  python run.py dev      # Servidor en modo desarrollo
  python run.py test     # Ejecutar pruebas
  python run.py install  # Instalar dependencias

📚 Documentación de la API:
  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc
  - Información: http://localhost:8000/
""")

if __name__ == "__main__":
    main()