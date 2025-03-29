from flask import Flask
from flask_cors import CORS
import os
from ninjaapp.routes import register_routes

app = Flask(__name__)
CORS(app)

# Registrar rutas desde el módulo
register_routes(app)

@app.route("/")
def home():
    return "🌐 NinjaApp está corriendo con estructura modular y lista para crecer."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
