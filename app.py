import os
import openai
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat con OpenAI</title>
</head>
<body>
    <h2>💬 Chat con OpenAI</h2>
    <form method="POST">
        <input name="prompt" placeholder="Escribe tu pregunta" style="width: 300px;">
        <button type="submit">Enviar</button>
    </form>
    {% if response %}
        <pre>{{ response }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response = completion.choices[0].message.content.strip()
        except Exception as e:
            response = f"⚠️ Error:\n{e}"

    return render_template_string(html_template, response=response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
