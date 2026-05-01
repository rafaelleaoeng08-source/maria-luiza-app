from flask import Flask, render_template, request, redirect
from flask import send_from_directory
import json
from datetime import datetime, timedelta
import requests
app = Flask(__name__)
# ======================
# ONESIGNAL CONFIG
# ======================

ONESIGNAL_APP_ID = "adc50cce-7803-4997-b030-16e794a792bb"
ONESIGNAL_API_KEY = "os_v2_app_vxcqzttyanezpmbqc3tzjj4sxpwx27fkhe7urg4i47q6voo344ajtqoz4sdmjrwc3agwvpwsi5c7clzz2c2xtqvi3ts4vsktqkiue6a"

# ======================
# BANCO DE DADOS
# ======================

def carregar():
    with open("banco_dados.json", "r") as f:
        return json.load(f)

def salvar(dados):
    with open("banco_dados.json", "w") as f:
        json.dump(dados, f, indent=4)
def enviar_notificacao(titulo, mensagem):
    url = "https://onesignal.com/api/v1/notifications"

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"
    }

    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["Total Subscriptions"],
        "headings": {"en": titulo},
        "contents": {"en": mensagem}
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
# ======================
# ROTAS
# ======================

@app.route("/")
def home():
    dados = carregar()
    return render_template("index.html", dados=dados)

# 💊 REMÉDIO (NOVO MODELO SIMPLES)
@app.route("/add_remedio", methods=["POST"])
def add_remedio():
    dados = carregar()

    nome = request.form["nome"]
    intervalo = int(request.form["intervalo"])
    inicio_str = request.form["inicio"]

    inicio = datetime.strptime(inicio_str, "%Y-%m-%dT%H:%M")
    proximo = inicio + timedelta(hours=intervalo)

    dados["medicamentos"].append({
        "nome": nome,
        "inicio": inicio_str,
        "intervalo": intervalo,
        "proximo": proximo.strftime("%Y-%m-%d %H:%M")
    })

    salvar(dados)
    return redirect("/", code=302)

# 🏥 CONSULTA (CORRIGIDO)
@app.route("/add_consulta", methods=["POST"])
def add_consulta():
    dados = carregar()

    dados["consultas"].append({
        "tipo": request.form["tipo"],
        "data": request.form["data"],
        "hora": request.form["hora"],
        "local": request.form.get("local", "")
    })

    salvar(dados)
    return redirect("/")

# 🍼 MAMADA
@app.route("/add_mamada", methods=["POST"])
def add_mamada():
    dados = carregar()

    dados["mamadas"].append({
        "horario": request.form["horario"]
    })

    salvar(dados)
    return redirect("/")
# 🗑️ EXCLUIR ITEM
@app.route("/delete/<tipo>/<int:index>")
def delete(tipo, index):
    dados = carregar()

    if tipo in dados and 0 <= index < len(dados[tipo]):
        dados[tipo].pop(index)

    salvar(dados)
    return redirect("/")
# ✔ ATUALIZAR REMÉDIO (JÁ DEU)
@app.route("/tomar_remedio/<int:index>")
def tomar_remedio(index):
    dados = carregar()

    if 0 <= index < len(dados["medicamentos"]):
        rem = dados["medicamentos"][index]

        intervalo = rem["intervalo"]

        # usa o último horário registrado
        ultimo = datetime.strptime(rem["inicio"], "%Y-%m-%dT%H:%M")

        # soma o intervalo
        novo = ultimo + timedelta(hours=intervalo)

        # atualiza corretamente
        rem["inicio"] = novo.strftime("%Y-%m-%dT%H:%M")
        rem["proximo"] = (novo + timedelta(hours=intervalo)).strftime("%Y-%m-%d %H:%M")

    salvar(dados)
    return redirect("/")

@app.route("/manifest.json")
def manifest():
    return app.send_static_file("manifest.json")

@app.route("/OneSignalSDKWorker.js")
def onesignal_worker():
    return send_from_directory("static", "OneSignalSDKWorker.js")

@app.route("/teste_notificacao")
def teste_notificacao():
    enviar_notificacao("Teste 🚀", "Chegou no celular!")
    return "Notificação enviada!"

if __name__ == "__main__":
    enviar_notificacao("Teste 🚀", "Notificação funcionando!")
    app.run()