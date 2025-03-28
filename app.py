from flask import Flask, request, jsonify, render_template_string
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Página principal con formulario
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>NinjaApp ✨</title>
        </head>
        <body>
            <h2>💬 Chat con OpenAI</h2>
            <input type="text" id="userInput" placeholder="Escribí tu pregunta" size="40">
            <button onclick="sendMessage()">Enviar</button>
            <pre id="response" style="margin-top:20px; background:#f0f0f0; padding:10px;"></pre>

            <script>
                async function sendMessage() {
                    const input = document.getElementById("userInput").value;
                    const res = await fetch("/api/chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ message: input })
                    });
                    const data = await res.json();
                    document.getElementById("response").textContent = data.reply;
                }
            </script>
        </body>
        </html>
    ''')

# Ruta para comunicarse con la API de OpenAI
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": user_message }]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({ "reply": reply })
    except Exception as e:
        return jsonify({ "reply": f"⚠️ Error: {str(e)}" })

# Línea sagrada para Railway 🙏🏼
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
