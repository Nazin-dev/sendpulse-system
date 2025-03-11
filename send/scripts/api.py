import os
import requests
from send.scripts import clients

CLIENT_ID = "f81d057b7359821b5a5e798c588e1c1b"
CLIENT_SECRET = "18b992701549c2831717e07ea387efcc"
API_URL = "https://api.sendpulse.com"

# Altere para True em ambiente de produção para enviar SMS de verdade.
SEND_SMS_ENABLED = False

def get_access_token():
    url = f"{API_URL}/oauth/access_token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("🆗 Token obtido com sucesso!")
        return response.json().get("access_token")
    else:
        print("❌ Erro ao obter token:", response.status_code, response.text)
        return None
  
token = get_access_token()
  
def send_sms(phone_numbers, message):
    # Verifica se o envio está habilitado
    if not SEND_SMS_ENABLED:
        print("Modo de desenvolvimento: SMS não será enviado.")
        print("Simulação de envio para:", phone_numbers, "com mensagem:", message)
        return

    access_token = token
    if not access_token:
        return print("Não temos o token")
  
    url = f"{API_URL}/sms/send"
  
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
  
    payload = {
        "sender": "RealSMS",
        "phones": phone_numbers,
        "body": message
    }
  
    response = requests.post(url, json=payload, headers=headers)
  
    if response.status_code == 200:
        print("✅ SMS enviado com sucesso!", response.json())
    else:
        print("❌ Erro ao enviar SMS:", response.status_code, response.text)
