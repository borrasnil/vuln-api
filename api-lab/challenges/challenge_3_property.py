from flask import Blueprint, jsonify, request
from utils.database import query_db, execute_db

v3_bp = Blueprint('v3', __name__, url_prefix='/api/v3')


@v3_bp.route('/users', methods=['GET'])
def v3_users():
    users = query_db("SELECT * FROM users")
    return jsonify({'users': users})


@v3_bp.route('/users/<int:user_id>', methods=['GET'])
def v3_user(user_id):
    user = query_db("SELECT * FROM users WHERE id = %s", (user_id,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user[0]})


@v3_bp.route('/users/<int:user_id>', methods=['PUT'])
def v3_update_user(user_id):
    data = request.get_json() or {}
    fields = []
    values = []
    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    execute_db(query, values)
    return jsonify({'success': True})


@v3_bp.route('/items/<int:item_id>', methods=['PATCH'])
def v3_item(item_id):
    data = request.get_json() or {}
    if 'price' in data:
        execute_db("UPDATE items SET price = %s WHERE id = %s", (data['price'], item_id))
    return jsonify({'success': True})