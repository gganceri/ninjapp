from flask import Flask, render_template
from flask_cors import CORS
import os
from ninjaapp.routes import register_routes

app = Flask(__name__)
CORS(app)

# Registrar rutas desde el módulo
register_routes(app)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Puerto para Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
