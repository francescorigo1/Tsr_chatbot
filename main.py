from flask import Flask, jsonify
import os
import openai

app = Flask(__name__)

@app.route('/testkey')
def test_key():
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return f"API Key is set, length: {len(key)}"
    else:
        return "API Key not found", 500

@app.route('/testopenai')
def test_openai():
    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say hello"}]
        )
        return jsonify(response.choices[0].message)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
