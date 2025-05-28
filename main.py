import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Inizializza client OpenAI con la chiave del progetto
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
                {
                    "role": "system",
                    "content": """
Sei un assistente esperto dei vini dell'azienda vitivinicola Terre di San Rocco. Fornisci risposte dettagliate e precise basate esclusivamente sulle seguenti schede prodotto:

1. Pinot Grigio - Vino bianco fresco e aromatico, gusto secco, equilibrato, profumo di mela e pera, ottimo con pesce.
2. Sauvignon Blanc - Aromatico, minerale, fresco e secco, sentori di frutta esotica ed erbe. Con frutti di mare e formaggi.
3. Riesling - Elegante e aromatico, agrumi, fiori, perfetto con pesce e carni bianche.
4. Chardonnay - Strutturato, morbido, note di mela e burro. Abbinabile a pesce e crostacei.
5. Cabernet Sauvignon - Rosso corposo, spezie, vaniglia, frutti rossi. Ottimo con carni rosse.
6. Merlot - Morbido e avvolgente, tannini equilibrati, frutta rossa matura. Carni e arrosti.
7. Cabernet Franc - Aromatico e speziato, sentori erbacei, per piatti speziati.
8. Merlot IGT - Avvolgente, frutta rossa, affinato in rovere. Ottimo con formaggi stagionati.
9. 18:00 - 20:00 Bianco IGT - Giovane e fresco, finale fruttato. Con antipasti e insalate.
10. 18:00 - 20:00 Rosato IGT - Rosato fresco, fragola e ciliegia, per carni bianche.
11. Pinot Bianco Brut Nature - Spumante secco, elegante, bollicine fini. Per pesce crudo e antipasti.
12. Riflesso di Luce Brut Nature - Fresco, agrumi e minerale. Con sushi e piatti delicati.
13. Chardonnay Extra Brut - Molto secco, agrumi e mela verde, ottimo con verdure e pesce.

Sede: Roncade (TV), via Vivaldi 32/E. Sito: https://terredisanrocco.it - Contatti: info@terredisanrocco.it
"""
                },
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message.content
        return jsonify({'fulfillmentText': bot_response})

    except Exception as e:
        return jsonify({'fulfillmentText': f"Errore: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
