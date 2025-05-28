from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Chiave API di OpenAI (deve essere settata su Render come variabile OPENAI_API_KEY)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Server è online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_message = req['queryResult']['queryText']

    try:
        # ChatGPT con istruzioni personalizzate per l'azienda vinicola
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente virtuale per l’azienda vinicola Terre di San Rocco. Rispondi solo su vini, degustazioni, metodi di produzione e visite in cantina."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = completion.choices[0].message['content']
        return jsonify({'fulfillmentText': bot_response})

    except Exception as e:
        # Stampa l'errore nei log e invia una risposta generica
        print(f"Errore OpenAI: {e}")
        return jsonify({'fulfillmentText': f"Scusa, c'è stato un errore: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
