import requests
import json

API_URL = "http://127.0.0.1:5001/ask-goodwe"


#user_question = "A luz acabou de cair! O que eu devo fazer para minha energia durar mais?"
#user_question = "Minha bateria vai durar a noite toda com esse consumo?"
user_question = "É uma boa ideia ligar a máquina de lavar agora?"

def make_request(query):
    print("="*50)
    print(f"🗣️  USUÁRIO (pergunta para a 'Alexa'): {query}")
    print("="*50)

    try:
        payload = {"query": query}
        
        response = requests.post(API_URL, json=payload)
        
        response.raise_for_status()
        
        response_data = response.json()
        ai_answer = response_data.get("response", "Nenhuma resposta recebida.")
        
        print("\n💡 ASSISTENTE GOODWE (resposta da 'Alexa'):")
        print(f"   {ai_answer}\n")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERRO: Não foi possível conectar à API em {API_URL}.")
        print(f"   Verifique se o servidor 'app.py' está rodando no terminal ao lado.")
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")

if __name__ == "__main__":
    make_request(user_question)