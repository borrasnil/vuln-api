from flask import Flask, jsonify, request
from routes.items import route

API_KEY = "$uP3r_$tR0nG_p4$$w0rd_M0nl4u2026"

app = Flask(__name__);

@app.before_request
def check_auth():
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_KEY}":
        return jsonify({'error': 'Unauthorized'}), 401

@app.get("/health")
def health():
    return "ok", 200

app.register_blueprint(route, url_prefix="/api")
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=3001
    )
   

