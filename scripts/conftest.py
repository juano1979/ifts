import os
import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Este hook se ejecuta al finalizar TODA la sesión de pruebas
def pytest_sessionfinish(session, exitstatus):
    """
    Se ejecuta después de que todos los tests han terminado.
    """
    # 1. Definimos la ruta del reporte (debe coincidir con la que uses al correr pytest)
    report_path = "reports/report.html"
    
    # 2. Obtenemos las credenciales de las variables de entorno
    token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL")

    # 3. Verificamos que el reporte exista y tengamos las credenciales
    if not os.path.exists(report_path):
        print(f"\n[Slack Hook] No se envió el reporte: No se encontró el archivo {report_path}")
        return

    if not token or not channel:
        print("\n[Slack Hook] No se envió el reporte: Faltan variables SLACK_TOKEN o SLACK_CHANNEL")
        return

    # 4. Enviamos a Slack
    client = WebClient(token=token)
    try:
        print(f"\n[Slack Hook] Enviando reporte final a Slack...")
        client.files_upload_v2(
            channel=channel,
            file=report_path,
            title="Reporte Automático de Tests",
            initial_comment=f"✅ Pruebas finalizadas. Estado de salida: {exitstatus} (0=Éxito, 1=Fallos)"
        )
        print("[Slack Hook] ¡Reporte enviado con éxito!")
    except SlackApiError as e:
        print(f"[Slack Hook] Error de Slack API: {e.response['error']}")
    except Exception as e:
        print(f"[Slack Hook] Error inesperado: {e}")