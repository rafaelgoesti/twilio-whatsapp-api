from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)
data = {"total": 0}

@app.route('/', methods=['POST'])
def whatsapp():
    global data

    msg = request.form.get('Body').strip()
    numero = request.form.get('From')
    resp = MessagingResponse()

    # Expressão regular para capturar um número decimal no final da mensagem
    match = re.search(r'(\d+(\.\d{1,2})?)$', msg)

    if match:
        gasto = float(match.group(1))
        data['total'] += gasto
        resp.message(f"*✅ Gasto adicionado: R${gasto:.2f}*\n*💸 Total acumulado: R${data['total']:.2f}*")
    else:
        resp.message("❌ Envie a descrição seguida do valor. Exemplo: Uber 25.60")

    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
