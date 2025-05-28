import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Inizializza client OpenAI con la chiave del progetto
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Link RAW al file su GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/francescorigo1/Tsr_chatbot/main/terre_di_san_rocco_info.txt"

# Funzione per scaricare il contenuto del file TXT da GitHub
def get_prompt_from_github():
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Errore scaricando il file: {e}")
        return None

# Scarica il prompt una volta all’avvio (puoi ricaricarlo periodicamente se vuoi)
system_prompt = get_prompt_from_github()
if not system_prompt:
    system_prompt = "Errore: non è stato possibile caricare le informazioni sui vini."

@app.route('/')
def home():
    return "Server è online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_message = req['queryResult']['queryText']

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message.content
        return jsonify({'fulfillmentText': bot_response})

    except Exception as e:
        return jsonify({'fulfillmentText': f"Errore: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
