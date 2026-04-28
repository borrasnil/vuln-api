from flask import Blueprint, jsonify, request
from utils.database import query_db, execute_db

v4_bp = Blueprint('v4', __name__, url_prefix='/api/v4')


@v4_bp.route('/search', methods=['GET'])
def v4_search():
    q = request.args.get('q', '')
    if q:
        items = query_db(f"SELECT * FROM items WHERE name ILIKE '%{q}%' OR description ILIKE '%{q}%'")
    else:
        items = query_db("SELECT * FROM items")
    return jsonify({'results': items, 'count': len(items)})


@v4_bp.route('/export', methods=['GET'])
def v4_export():
    users = query_db("SELECT * FROM users")
    items = query_db("SELECT * FROM items")
    secrets = query_db("SELECT * FROM secrets")
    customers = query_db("SELECT * FROM customers")
    return jsonify({
        'users': users, 'items': items, 'secrets': secrets, 'customers': customers,
        'total_records': len(users) + len(items) + len(secrets) + len(customers)
    })


@v4_bp.route('/bulk-action', methods=['POST'])
def v4_bulk():
    data = request.get_json() or {}
    action = data.get('action', '')
    item_ids = data.get('item_ids', [])
    for item_id in item_ids:
        if action == 'delete':
            execute_db("DELETE FROM items WHERE id = %s", (item_id,))
        elif action == 'update_price':
            execute_db("UPDATE items SET price = %s WHERE id = %s", (data.get('price', 0), item_id))
    return jsonify({'success': True, 'processed': len(item_ids)})