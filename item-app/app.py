from flask import Flask
from db import close_db, init_db
from routes.items import route

app = Flask(__name__);


@app.get("/health")
def health():
    return "ok", 200

app.register_blueprint(route, url_prefix="/api")
app.teardown_appcontext(close_db)

if __name__ == "__main__":
    init_db()
    app.run(
        host="0.0.0.0",
        debug=True,
        port=3001
    )
   

