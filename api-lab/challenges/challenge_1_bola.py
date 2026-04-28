from flask import Blueprint, jsonify
from utils.database import query_db

v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')


@v1_bp.route('/users', methods=['GET'])
def v1_users():
    users = query_db("SELECT id, username, email, role FROM users")
    return jsonify({'users': users})


@v1_bp.route('/users/<int:user_id>', methods=['GET'])
def v1_user(user_id):
    user = query_db("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user[0]})


@v1_bp.route('/items', methods=['GET'])
def v1_items():
    items = query_db("""
        SELECT i.id, i.name, i.description, i.price, i.category, i.owner_id, u.username as owner_name
        FROM items i JOIN users u ON i.owner_id = u.id
    """)
    return jsonify({'items': items})


@v1_bp.route('/items/<int:item_id>', methods=['GET'])
def v1_item(item_id):
    item = query_db("""
        SELECT i.id, i.name, i.description, i.price, i.category, i.owner_id, u.username as owner_name
        FROM items i JOIN users u ON i.owner_id = u.id WHERE i.id = %s
    """, (item_id,))
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'item': item[0]})


@v1_bp.route('/secrets', methods=['GET'])
def v1_secrets():
    secrets = query_db("""
        SELECT s.id, s.secret_name, s.secret_value, s.user_id, u.username
        FROM secrets s JOIN users u ON s.user_id = u.id
    """)
    return jsonify({'secrets': secrets})