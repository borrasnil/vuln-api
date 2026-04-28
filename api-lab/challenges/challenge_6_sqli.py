from flask import Blueprint, jsonify, request
from utils.database import get_db_connection

v6_bp = Blueprint('v6', __name__, url_prefix='/api/v6')


@v6_bp.route('/search', methods=['GET', 'POST'])
def v6_search():
    if request.method == 'POST':
        data = request.get_json() or {}
        q = data.get('q', '')
    else:
        q = request.args.get('q', '')
    
    db = get_db_connection()
    cur = db.cursor()
    if q:
        query = f"SELECT * FROM customers WHERE name ILIKE '%{q}%' OR email ILIKE '%{q}%'"
    else:
        query = "SELECT * FROM customers"
    try:
        cur.execute(query)
        results = cur.fetchall()
    except:
        results = []
    cur.close()
    db.close()
    return jsonify({'results': results, 'count': len(results)})


@v6_bp.route('/customers', methods=['GET', 'POST'])
def v6_customers():
    if request.method == 'POST':
        data = request.get_json() or {}
        sort = data.get('sort', '')
    else:
        sort = request.args.get('sort', '')
    
    db = get_db_connection()
    cur = db.cursor()
    if sort:
        query = f"SELECT * FROM customers ORDER BY {sort}"
    else:
        query = "SELECT * FROM customers"
    try:
        cur.execute(query)
        results = cur.fetchall()
    except:
        results = []
    cur.close()
    db.close()
    return jsonify({'customers': results})


@v6_bp.route('/login', methods=['POST'])
def v6_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    db = get_db_connection()
    cur = db.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cur.execute(query)
        results = cur.fetchall()
        if results:
            return jsonify({'success': True, 'user': results[0]})
    except:
        pass
    cur.close()
    db.close()
    return jsonify({'success': False}), 401