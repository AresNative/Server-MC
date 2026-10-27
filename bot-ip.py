import requests
import time
import os

# --- CONFIGURACIÓN ---
WEBHOOK_URL = "PEGA_AQUI_TU_URL_DE_WEBHOOK"
INTERVALO_SEGUNDOS = 300  # Revisar cada 5 minutos
ARCHIVO_ULTIMA_IP = "ultima_ip.txt"
# ---------------------

def obtener_ip_publica():
    try:
        # Usamos ipify, un servicio simple y confiable
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        response.raise_for_status()
        return response.json()['ip']
    except Exception as e:
        print(f"Error al obtener la IP: {e}")
        return None

def enviar_discord(ip):
    data = {
        "content": f"🌐 ¡Tu IP pública ha cambiado! Nueva IP: **{ip}**:25565"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=10)
        response.raise_for_status()
        print(f"Notificación enviada a Discord. Nueva IP: {ip}")
    except Exception as e:
        print(f"Error al enviar a Discord: {e}")

def main():
    print("Iniciando monitor de IP...")
    # Leer la última IP guardada
    if os.path.exists(ARCHIVO_ULTIMA_IP):
        with open(ARCHIVO_ULTIMA_IP, 'r') as f:
            ultima_ip = f.read().strip()
    else:
        ultima_ip = None

    while True:
        ip_actual = obtener_ip_publica()
        if ip_actual and ip_actual != ultima_ip:
            print(f"IP cambiada de {ultima_ip} a {ip_actual}")
            enviar_discord(ip_actual)
            with open(ARCHIVO_ULTIMA_IP, 'w') as f:
                f.write(ip_actual)
            ultima_ip = ip_actual
        elif ip_actual:
            print(f"IP sin cambios: {ip_actual}")
        
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
