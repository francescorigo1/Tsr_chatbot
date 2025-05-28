from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Server è online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    user_message = req['queryResult']['queryText']

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_response = completion.choices[0].message['content']
        return jsonify({'fulfillmentText': bot_response})

    except Exception as e:
        print(f"Errore OpenAI: {e}")
        return jsonify({'fulfillmentText': 'Scusa, c\'è stato un errore nel processare la tua richiesta.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
