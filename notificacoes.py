import requests
import json

# 🔴 COLE AQUI SEUS DADOS DO ONESIGNAL
ONESIGNAL_APP_ID = "adc50cce-7803-4997-b030-16e794a792bb"
ONESIGNAL_REST_API_KEY = "os_v2_app_vxcqzttyanezpmbqc3tzjj4sxpjhn22yg2lebnuhm5ywqeavkz6s4gxkripzaevs3gpwpu4tajtw43xili3wtdk3jkemvpg3uez27za"


def enviar_notificacao():
    url = "https://onesignal.com/api/v1/notifications"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,

        # 👇 ESSA LINHA É A MAIS IMPORTANTE
        "included_segments": ["All"],

        "headings": {"en": "Maria Luiza 💖"},
        "contents": {"en": "Teste automático funcionando 🚀"}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print("Status:", response.status_code)
    print("Resposta:", response.text)

    return response.text