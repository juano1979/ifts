#!/usr/bin/env python3
import os
import sys
# Cambiamos requests por la librería oficial de Slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def upload_file(token: str, channel: str, file_path: str) -> None:
    # Inicializamos el cliente oficial
    client = WebClient(token=token)
    
    try:
        print(f"Subiendo {file_path} a Slack...")
        
        # Usamos files_upload_v2 que arregla el error 'method_deprecated'
        # Esta función maneja internamente toda la nueva lógica de Slack
        response = client.files_upload_v2(
            channel=channel,
            file=file_path,
            title="Reporte Automático",
            initial_comment="🚀 Aquí está el reporte actualizado."
        )
        
        if response["ok"]:
            print("¡Reporte subido a Slack con éxito!")
            
    except SlackApiError as e:
        # Si el error es de la API de Slack (ej: token inválido)
        raise SystemExit(f"Error de la API de Slack: {e.response['error']}")
    except Exception as e:
        # Otros errores (ej: archivo no encontrado)
        raise SystemExit(f"Error inesperado: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 send_slack_report.py <ruta-del-reporte>")
        sys.exit(2)
        
    path = sys.argv[1]
    token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")
    
    if not token or not channel:
        print("Faltan variables de entorno: SLACK_TOKEN y SLACK_CHANNEL")
        sys.exit(2)
        
    if not os.path.exists(path):
        print(f"El reporte no existe en la ruta: {path}")
        sys.exit(2)
        
    upload_file(token, channel, path)

if __name__ == "__main__":
    main()