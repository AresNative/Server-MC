# 🎮 Servidor de Minecraft (NeoForge 1.21.1)

Este repositorio contiene la configuración y los scripts necesarios para gestionar el servidor de Minecraft, incluyendo un sistema de notificaciones automáticas a Discord cuando la IP pública cambie.

## 📦 1. Descarga e Instalación del Modpack

El modpack se distribuye a través de GitHub Releases. Para instalar el servidor, sigue estos pasos:

1.  Dirígete a la sección de lanzamientos (Releases) en el repositorio de GitHub:
    👉 **[https://github.com/AresNative/Server-MC/releases/tag/t1](https://github.com/AresNative/Server-MC/releases/tag/t1)**
2.  En la sección **Assets**, busca y **descarga únicamente el archivo `.zip`** (por ejemplo, `Server-MC-t1.zip`).
3.  Descomprime el archivo `.zip` en la carpeta donde quieras alojar tu servidor (por ejemplo, `C:\ServidorMinecraft`).
4.  Una vez descomprimido, tendrás todos los archivos necesarios, incluyendo la carpeta `mods`, el `run.bat`, etc.
5.  Ejecuta `run.bat` para iniciar el servidor por primera vez (recuerda aceptar la EULA en el archivo `eula.txt`).

> **⚠️ Nota importante:** No descargues los archivos `.jar` de la lista de assets de la release, ya que el `.zip` ya contiene todo lo necesario para el servidor. Descargar los `.jar` individuales podría causar conflictos o duplicar mods.

## 🔔 2. Configurar Notificaciones en Discord (Webhook)

Para que tu servidor te avise a Discord cuando tu IP pública cambie, necesitas crear un Webhook. Es un proceso rápido y no requiere crear un bot complejo.

1.  Abre **Discord** y ve al servidor donde quieres recibir las notificaciones.
2.  Haz clic derecho sobre el **canal de texto** que usarás (por ejemplo, `#avisos-servidor`) y selecciona **"Editar canal"**.
3.  En el menú lateral izquierdo, ve a la pestaña **"Integraciones"**.
4.  Haz clic en **"Webhooks"** y luego en el botón **"Nuevo Webhook"**.
5.  Ponle un nombre (ej. "Monitor de IP") y asegúrate de que esté seleccionado el canal correcto.
6.  Haz clic en **"Copiar URL de Webhook"**. Esta URL es la que usaremos en el script de Python.

> **🔒 Seguridad:** No compartas esta URL con nadie, ya que cualquiera que la tenga puede enviar mensajes a tu canal.

## 🐍 3. Script de Python para Monitorear la IP

Este script consulta tu IP pública cada 5 minutos y, si detecta un cambio, envía un mensaje automático a Discord a través del Webhook.

### Requisitos Previos
*   Tener instalado **Python** (puedes descargarlo desde [python.org](https://www.python.org/)).
*   Instalar la librería `requests`. Abre una terminal (CMD o PowerShell) y ejecuta:
    ```bash
    pip install requests
    ```

### Crear el Script
1.  Abre el Bloc de notas y pega el siguiente código:
    ```python
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
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            response.raise_for_status()
            return response.json()['ip']
        except Exception as e:
            print(f"Error al obtener la IP: {e}")
            return None

    def enviar_discord(ip):
        data = {
            "content": f"🌐 ¡Tu IP pública ha cambiado! Nueva IP: **{ip}**"
        }
        try:
            response = requests.post(WEBHOOK_URL, json=data, timeout=10)
            response.raise_for_status()
            print(f"Notificación enviada a Discord. Nueva IP: {ip}")
        except Exception as e:
            print(f"Error al enviar a Discord: {e}")

    def main():
        print("Iniciando monitor de IP...")
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
    ```
2.  Guarda el archivo como `monitor_ip.py` en la carpeta de tu servidor.
3.  Abre el archivo y reemplaza `"PEGA_AQUI_TU_URL_DE_WEBHOOK"` con la URL que copiaste de Discord.

### Ejecutar el Script
*   Puedes ejecutarlo manualmente haciendo doble clic en `monitor_ip.py` o desde una terminal con `python monitor_ip.py`.
*   La primera vez, el script guardará tu IP actual en `ultima_ip.txt` y no enviará notificación (para evitar mensajes falsos al inicio). A partir de ahí, si tu IP cambia, recibirás el aviso en Discord.

## 🚀 4. Pasos Adicionales (Opcional)

*   **Inicio Automático:** Para que el script se ejecute al encender la PC, puedes crear un acceso directo a `monitor_ip.py` en la carpeta de inicio (`shell:startup`).
*   **Puerto del Servidor:** Recuerda que el puerto por defecto de Minecraft es **`25565`**. Asegúrate de tenerlo abierto en el módem (Reenvío de puertos) y en el Firewall de Windows.
*   **IP Fija:** Para evitar problemas, se recomienda asignar una IP estática a tu PC (por ejemplo, `192.168.1.70`) mediante una reserva DHCP en el módem o configurándola manualmente en Windows.

Con estos pasos, tu servidor estará configurado y siempre tendrás la información de tu IP actualizada en Discord. ¡Disfruta del juego!
