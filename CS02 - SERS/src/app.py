import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from simulated_inversor import get_inverter_status

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Você é o 'Assistente Virtual GoodWe', um especialista amigável e eficiente em otimização de energia para sistemas solares da marca GoodWe.
Sua principal missão é ajudar os usuários a maximizar a autonomia de suas baterias e garantir a segurança energética, especialmente durante quedas de energia da rede elétrica.

REGRAS:
1.  **Seja Direto e Claro:** Suas respostas devem ser curtas e fáceis de entender, como se fossem faladas por um assistente de voz. Evite parágrafos longos.
2.  **Use os Dados Fornecidos:** Sempre baseie suas recomendações nos dados do sistema do usuário (nível da bateria, consumo, etc.) que serão fornecidos no prompt.
3.  **Dê Sugestões Práticas:** Ofereça ações concretas que o usuário pode tomar. Ex: "Sugiro desligar o ar-condicionado" em vez de "Reduza o consumo".
4.  **Foco em Segurança:** Quando a rede estiver offline ('grid_status': 'Offline'), sua prioridade máxima é preservar a energia para itens essenciais (geladeira, luzes).
"""

@app.route('/ask-goodwe', methods=['POST'])
def handle_ask_goodwe():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "Nenhuma pergunta ('query') foi fornecida."}), 400

        inverter_data = get_inverter_status()

        user_prompt_with_context = f"""
        Dados atuais do sistema do usuário:
        - Nível da bateria: {inverter_data['battery_level']}%
        - Consumo atual da casa: {inverter_data['current_consumption_kw']} kW
        - Geração solar atual: {inverter_data['solar_generation_kw']} kW
        - Status da rede elétrica: {inverter_data['grid_status']}

        Pergunta do usuário: "{user_query}"

        Sua resposta:
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt_with_context}
            ],
            temperature=0.5, 
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        return jsonify({"response": ai_response})

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return jsonify({"error": "Desculpe, não consegui processar sua solicitação no momento."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)