from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
from decimal import Decimal, InvalidOperation

app = Flask(__name__)

# Estrutura para armazenar os dados de forma mais organizada
expense_data = {
    "total": Decimal('0.00'),
    "transactions": []
}

@app.route('/', methods=['POST'])
def whatsapp():
    msg = request.form.get('Body', '').strip()
    numero = request.form.get('From')
    resp = MessagingResponse()

    # Expressão regular melhorada para capturar valores monetários
    # Aceita formatos como 25, 25.60, 25.6, 1000.00
    match = re.search(r'(\d+([.,]\d{1,2})?)$', msg)

    if match:
        try:
            # Substitui vírgula por ponto para padronização
            value_str = match.group(1).replace(',', '.')
            gasto = Decimal(value_str).quantize(Decimal('0.00'))
            
            # Atualiza os dados
            expense_data['total'] += gasto
            expense_data['transactions'].append({
                'value': gasto,
                'description': msg[:match.start()].strip(),
                'from': numero
            })
            
            # Formata a resposta com emojis e valores alinhados
            response_msg = (
                f"✅ *Registro adicionado:* {msg[:match.start()].strip() or 'Sem descrição'}\n"
                f"💵 *Valor:* R$ {gasto:.2f}\n\n"
                f"💰 *Total acumulado:* R$ {expense_data['total']:.2f}"
            )
            resp.message(response_msg)
            
        except InvalidOperation:
            resp.message("❌ *Formato inválido.* Por favor, envie no formato: 'Descrição valor'.\nExemplo: 'Almoço 25.60'")
    else:
        # Mensagem de ajuda mais completa
        help_msg = (
            "📋 *Como registrar um gasto:*\n\n"
            "Envie a descrição seguida do valor.\n"
            "• Exemplo 1: 'Táxi 25.60'\n"
            "• Exemplo 2: 'Supermercado 150,00'\n\n"
            "⚠️ O valor deve ser numérico, com até 2 casas decimais."
        )
        resp.message(help_msg)

    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)