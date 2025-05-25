from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)
data = {"total": 0}

@app.route('/', methods=['POST'])
def whatsapp():
    global data

    msg = request.form.get('Body') 
    numero = request.form.get('From')
    resp = MessagingResponse()

    try:
        gasto = float(msg)
        data['total'] += gasto
        resp.message(f"*✅Gasto adicionado: R${gasto:.2f}*\n*💸 Total acumulado: R${data['total']:.2f}*")

        # with open('gastos.json', 'w') as f:
        #    json.dump(data, f)

    except:
        resp.message("❌ Envie apenas o valor do gasto. Exemplo: 25.50")

    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
