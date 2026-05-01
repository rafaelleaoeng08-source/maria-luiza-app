import requests
import json

# 🔴 COLE AQUI SEUS DADOS DO ONESIGNAL
ONESIGNAL_APP_ID = "adc50cce-7803-4997-b030-16e794a792bb"
ONESIGNAL_REST_API_KEY = "os_v2_app_vxcqzttyanezpmbqc3tzjj4sxpwx27fkhe7urg4i47q6voo344ajtqoz4sdmjrwc3agwvpwsi5c7clzz2c2xtqvi3ts4vsktqkiue6a"


def enviar_notificacao():
    url = "https://onesignal.com/api/v1/notifications"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,

        # 👇 ESSA LINHA É A MAIS IMPORTANTE
        "included_segments": ["Subscribed Users"],

        "headings": {"en": "Maria Luiza 💖"},
        "contents": {"en": "Teste automático funcionando 🚀"}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status:", response.status_code)
    print("Resposta:", response.text)

    return response.text