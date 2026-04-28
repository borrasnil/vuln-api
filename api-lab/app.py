import os
from flask import Flask, jsonify
from challenges import v1_bp, v2_bp, v3_bp, v4_bp, v5_bp, v6_bp
from utils.database import close_db

app = Flask(__name__)

app.register_blueprint(v1_bp)
app.register_blueprint(v2_bp)
app.register_blueprint(v3_bp)
app.register_blueprint(v4_bp)
app.register_blueprint(v5_bp)
app.register_blueprint(v6_bp)


@app.teardown_appcontext
def teardown_db(error):
    close_db(error)


@app.route('/api/')
def api_index():
    from models.challenges import CHALLENGES
    return jsonify({
        'challenges': {str(k): v['name'] for k, v in CHALLENGES.items()}
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')