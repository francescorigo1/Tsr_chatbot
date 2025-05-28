import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Inizializza client OpenAI con la chiave del progetto
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Carica il contenuto del prompt da file al momento dell’avvio
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

@app.route('/')
def home():
    return "Server è online!"

@app.route('/testopenai')
def test_openai():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say hello!"}
            ]
        )
        return jsonify(response.choices[0].message.dict())
    except Exception as e:
        return jsonify({"error": str(e)})

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
