from flask import Flask, render_template_string, request
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Chat con OpenAI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #f3f4f6;
            font-family: 'Inter', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .chat-box {
            background: white;
            padding: 2rem;
            border-radius: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
            text-align: center;
            animation: fadeIn 1.2s ease;
        }
        h1 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        input[type="text"] {
            width: 70%;
            padding: 0.6rem;
            border: 2px solid #e5e7eb;
            border-radius: 1rem;
            margin-bottom: 1rem;
            font-size: 1rem;
            transition: border 0.3s;
        }
        input[type="text"]:focus {
            border-color: #6366f1;
            outline: none;
        }
        input[type="submit"] {
            padding: 0.6rem 1.2rem;
            border: none;
            background-color: #6366f1;
            color: white;
            font-weight: 600;
            border-radius: 1rem;
            cursor: pointer;
            transition: background 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #4f46e5;
        }
        .response {
            margin-top: 1rem;
            font-size: 1rem;
            color: #333;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="chat-box">
        <h1>💬 Chat con OpenAI</h1>
        <form method="post">
            <input type="text" name="prompt" placeholder="Escribe tu pregunta" required>
            <input type="submit" value="Enviar">
        </form>
        {% if response %}
            <div class="response">{{ response }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
