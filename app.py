from flask import Flask, request, render_template_string
import openai
import os

app = Flask(__name__)

# Configurar la clave API desde variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

html_template = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat con OpenAI</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f7f7f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            animation: fadeIn 1s ease-in;
        }
        .chat-box {
            background: white;
            padding: 2rem;
            border-radius: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            text-align: center;
            animation: slideUp 0.7s ease-in-out;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            padding: 0.6rem;
            border: 1px solid #ccc;
            border-radius: 20px;
            width: 60%;
            margin-right: 0.5rem;
        }
        button {
            padding: 0.6rem 1.2rem;
            background-color: #6c47ff;
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #583ad6;
        }
        p {
            margin-top: 1rem;
            color: #333;
        }
        .error {
            color: red;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(40px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="chat-box">
        <h1>💬 Chat con OpenAI</h1>
        <form method="POST">
            <input type="text" name="message" placeholder="Escribe tu pregunta" required>
            <button type="submit">Enviar</button>
        </form>
        {% if response %}
            <p><strong>Respuesta:</strong> {{ response }}</p>
        {% endif %}
        {% if error %}
            <p class="error"><strong>Error:</strong> {{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    error = ""
    if request.method == "POST":
        user_message = request.form["message"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            response = completion.choices[0].message.content
        except Exception as e:
            error = str(e)
    return render_template_string(html_template, response=response, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
