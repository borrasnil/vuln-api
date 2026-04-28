from flask import Blueprint, jsonify, request
from utils.database import query_db, execute_db

v2_bp = Blueprint('v2', __name__, url_prefix='/api/v2')


@v2_bp.route('/login', methods=['POST'])
def v2_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    user = query_db(f"SELECT id, username, email, role FROM users WHERE username = '{username}' AND password = '{password}'")
    if user:
        return jsonify({'success': True, 'user': user[0]})
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@v2_bp.route('/register', methods=['POST'])
def v2_register():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', '')
    execute_db("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)", (username, password, email, 'user'))
    return jsonify({'success': True, 'message': 'User registered'}), 201


@v2_bp.route('/reset-password', methods=['POST'])
def v2_reset():
    data = request.get_json() or {}
    username = data.get('username', '')
    new_password = data.get('new_password', '')
    execute_db("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    return jsonify({'success': True, 'message': f'Password reset for {username}'})