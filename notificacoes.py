import requests
import json

# 🔴 COLE AQUI SEUS DADOS DO ONESIGNAL
ONESIGNAL_APP_ID = "adc50cce-7803-4997-b030-16e794a792bb"
ONESIGNAL_REST_API_KEY = "os_v2_app_vxcqzttyanezpmbqc3tzjj4sxpbrged7mf2ecwnhbriufpzhhvra75z4qwwzkfefg2auzvgv5dig6yzwihug4uzfbutuhatvh2sbozi"


def enviar_notificacao():
    url = "https://api.onesignal.com/notifications"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Key {ONESIGNAL_REST_API_KEY}"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "headings": {"en": "Maria Luiza 💖"},
        "contents": {"en": "Teste automático funcionando 🚀"}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status:", response.status_code)
    print("Resposta:", response.text)

    return response.text