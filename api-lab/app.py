import os
import re
from flask import Flask, request, jsonify, g, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://api_user:api_pass@postgres:5432/api_lab')

CHALLENGES = {
    1: {
        'name': 'Broken Object Level Authorization',
        'short': 'BOLA / IDOR',
        'description': 'Access other users\' resources by manipulating object IDs',
        'severity': 'Critical',
        'explanation': 'APIs expose endpoints that handle object identifiers without verifying ownership. Any user can access anyone else\'s data by changing the ID in the URL.',
        'why_vulnerable': 'No ownership check on resource access\nTrusting user-provided IDs\nLack of authorization at object level',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v1/users', 'desc': 'List all users'},
            {'method': 'GET', 'path': '/api/v1/users/{id}', 'desc': 'Get user by ID'},
            {'method': 'GET', 'path': '/api/v1/items', 'desc': 'List all items'},
            {'method': 'GET', 'path': '/api/v1/items/{id}', 'desc': 'Get item by ID'},
            {'method': 'GET', 'path': '/api/v1/secrets', 'desc': 'List all secrets'},
        ]
    },
    2: {
        'name': 'Broken Authentication',
        'short': 'Broken Auth',
        'description': 'Flawed login allowing account takeover and brute force attacks',
        'severity': 'Critical',
        'explanation': 'Flawed login mechanisms allowing account takeover, brute force attacks, token manipulation, and session hijacking.',
        'why_vulnerable': 'No rate limiting\nNo account lockout\nWeak password policies\nNo verification on password reset',
        'endpoints': [
            {'method': 'POST', 'path': '/api/v2/login', 'desc': 'Login'},
            {'method': 'POST', 'path': '/api/v2/register', 'desc': 'Register new user'},
            {'method': 'POST', 'path': '/api/v2/reset-password', 'desc': 'Reset password'},
        ]
    },
    3: {
        'name': 'Broken Object Property Level Auth',
        'short': 'Property Auth',
        'description': 'Excessive data exposure and mass assignment vulnerabilities',
        'severity': 'High',
        'explanation': 'API returns all fields including sensitive data (passwords, secrets) and allows users to modify privileged fields like role and admin status.',
        'why_vulnerable': 'No field-level filtering\nDirect parameter binding\nNo allowlist for sensitive fields',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v3/users', 'desc': 'List users (exposes password)'},
            {'method': 'GET', 'path': '/api/v3/users/{id}', 'desc': 'Get user details'},
            {'method': 'PUT', 'path': '/api/v3/users/{id}', 'desc': 'Update user (mass assignment)'},
            {'method': 'PATCH', 'path': '/api/v3/items/{id}', 'desc': 'Update item price'},
        ]
    },
    4: {
        'name': 'Unrestricted Resource Consumption',
        'short': 'Resource',
        'description': 'No rate limiting allowing DoS and cost escalation',
        'severity': 'High',
        'explanation': 'No rate limiting allowing DoS attacks via excessive API calls or cost escalation through expensive operations.',
        'why_vulnerable': 'No request limits\nNo pagination\nNo timeout on expensive operations',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v4/search?q=query', 'desc': 'Search (no limit)'},
            {'method': 'GET', 'path': '/api/v4/export', 'desc': 'Export all data'},
            {'method': 'POST', 'path': '/api/v4/bulk-action', 'desc': 'Bulk operations'},
        ]
    },
    5: {
        'name': 'Server-Side Request Forgery',
        'short': 'SSRF',
        'description': 'API fetches user URLs enabling internal network attacks',
        'severity': 'High',
        'explanation': 'API fetches user-controlled URLs enabling internal network attacks, cloud metadata access, and port scanning.',
        'why_vulnerable': 'No URL validation\nBlind trust of user input\nFollowing redirects',
        'endpoints': [
            {'method': 'POST', 'path': '/api/v5/fetch', 'desc': 'Fetch URL'},
            {'method': 'GET', 'path': '/api/v5/proxy', 'desc': 'Proxy request'},
            {'method': 'POST', 'path': '/api/v5/webhook', 'desc': 'Set webhook'},
        ]
    },
    6: {
        'name': 'SQL Injection',
        'short': 'SQLi',
        'description': 'Direct SQL concatenation allowing data extraction',
        'severity': 'Critical',
        'explanation': 'Classic SQL injection allowing data extraction, authentication bypass, and potential database takeover.',
        'why_vulnerable': 'String concatenation in queries\nNo input sanitization\nNo parameterized queries',
        'endpoints': [
            {'method': 'GET', 'path': '/api/v6/search?q=query', 'desc': 'Search'},
            {'method': 'GET', 'path': '/api/v6/customers', 'desc': 'List customers'},
            {'method': 'POST', 'path': '/api/v6/login', 'desc': 'Login (SQLi bypass)'},
        ]
    }
}

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

def query_db(query, args=None):
    if args is None:
        args = ()
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
    except Exception as e:
        rv = []
    cur.close()
    return rv

def execute_db(query, args=None):
    if args is None:
        args = ()
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, args)
        db.commit()
    except Exception:
        db.rollback()
    cur.close()

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('index.html', challenges=CHALLENGES)

@app.route('/challenge/<int:id>')
def challenge(id):
    if id not in CHALLENGES:
        return "Challenge not found", 404
    return render_template('challenge.html', challenge=CHALLENGES[id], id=id, challenges=CHALLENGES)

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/')
def api_index():
    return jsonify({
        'challenges': {str(k): v['name'] for k, v in CHALLENGES.items()}
    })

# --- Challenge 1: BOLA ---
@app.route('/api/v1/users', methods=['GET'])
def v1_users():
    users = query_db("SELECT id, username, email, role FROM users")
    return jsonify({'users': users})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def v1_user(user_id):
    user = query_db("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user[0]})

@app.route('/api/v1/items', methods=['GET'])
def v1_items():
    items = query_db("""
        SELECT i.id, i.name, i.description, i.price, i.category, i.owner_id, u.username as owner_name
        FROM items i JOIN users u ON i.owner_id = u.id
    """)
    return jsonify({'items': items})

@app.route('/api/v1/items/<int:item_id>', methods=['GET'])
def v1_item(item_id):
    item = query_db("""
        SELECT i.id, i.name, i.description, i.price, i.category, i.owner_id, u.username as owner_name
        FROM items i JOIN users u ON i.owner_id = u.id WHERE i.id = %s
    """, (item_id,))
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'item': item[0]})

@app.route('/api/v1/secrets', methods=['GET'])
def v1_secrets():
    secrets = query_db("""
        SELECT s.id, s.secret_name, s.secret_value, s.user_id, u.username
        FROM secrets s JOIN users u ON s.user_id = u.id
    """)
    return jsonify({'secrets': secrets})

# --- Challenge 2: Auth ---
@app.route('/api/v2/login', methods=['POST'])
def v2_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    user = query_db("SELECT id, username, email, role FROM users WHERE username = %s AND password = %s", (username, password))
    if user:
        return jsonify({'success': True, 'user': user[0]})
    return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/v2/register', methods=['POST'])
def v2_register():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    email = data.get('email', '')
    execute_db("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)", (username, password, email, 'user'))
    return jsonify({'success': True, 'message': 'User registered'}), 201

@app.route('/api/v2/reset-password', methods=['POST'])
def v2_reset():
    data = request.get_json() or {}
    username = data.get('username', '')
    new_password = data.get('new_password', '')
    execute_db("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
    return jsonify({'success': True, 'message': f'Password reset for {username}'})

# --- Challenge 3: Property Auth ---
@app.route('/api/v3/users', methods=['GET'])
def v3_users():
    users = query_db("SELECT * FROM users")
    return jsonify({'users': users})

@app.route('/api/v3/users/<int:user_id>', methods=['GET'])
def v3_user(user_id):
    user = query_db("SELECT * FROM users WHERE id = %s", (user_id,))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user[0]})

@app.route('/api/v3/users/<int:user_id>', methods=['PUT'])
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

@app.route('/api/v3/items/<int:item_id>', methods=['PATCH'])
def v3_item(item_id):
    data = request.get_json() or {}
    if 'price' in data:
        execute_db("UPDATE items SET price = %s WHERE id = %s", (data['price'], item_id))
    return jsonify({'success': True})

# --- Challenge 4: Resource ---
@app.route('/api/v4/search', methods=['GET'])
def v4_search():
    q = request.args.get('q', '')
    if q:
        q_safe = q.replace("'", "''")
        items = query_db(f"SELECT * FROM items WHERE name ILIKE '%{q_safe}%' OR description ILIKE '%{q_safe}%'")
    else:
        items = query_db("SELECT * FROM items")
    return jsonify({'results': items, 'count': len(items)})

@app.route('/api/v4/export', methods=['GET'])
def v4_export():
    users = query_db("SELECT * FROM users")
    items = query_db("SELECT * FROM items")
    secrets = query_db("SELECT * FROM secrets")
    customers = query_db("SELECT * FROM customers")
    return jsonify({
        'users': users, 'items': items, 'secrets': secrets, 'customers': customers,
        'total_records': len(users) + len(items) + len(secrets) + len(customers)
    })

@app.route('/api/v4/bulk-action', methods=['POST'])
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

# --- Challenge 5: SSRF ---
@app.route('/api/v5/fetch', methods=['POST'])
def v5_fetch():
    data = request.get_json() or {}
    url = data.get('url', '')
    return jsonify({'success': True, 'fetched_url': url, 'message': f'URL {url} fetched'})

@app.route('/api/v5/proxy', methods=['GET'])
def v5_proxy():
    url = request.args.get('url', '')
    return jsonify({'proxy_to': url})

@app.route('/api/v5/webhook', methods=['POST'])
def v5_webhook():
    data = request.get_json() or {}
    return jsonify({'success': True, 'webhook': data.get('webhook_url')})

# --- Challenge 6: SQLi ---
@app.route('/api/v6/search', methods=['GET', 'POST'])
def v6_search():
    # Accept SQLi payloads in both GET and POST
    if request.method == 'POST':
        data = request.get_json() or {}
        q = data.get('q', '')
    else:
        q = request.args.get('q', '')
    
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    if q:
        # SQLi vulnerable - direct concatenation
        query = f"SELECT * FROM customers WHERE name ILIKE '%{q}%' OR email ILIKE '%{q}%'"
    else:
        query = "SELECT * FROM customers"
    try:
        cur.execute(query)
        results = cur.fetchall()
    except:
        results = []
    cur.close()
    return jsonify({'results': results, 'count': len(results)})

@app.route('/api/v6/customers', methods=['GET', 'POST'])
def v6_customers():
    # Accept SQLi via both GET and POST
    if request.method == 'POST':
        data = request.get_json() or {}
        sort = data.get('sort', '')
    else:
        sort = request.args.get('sort', '')
    
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    if sort:
        # SQLi vulnerable - direct column name injection
        query = f"SELECT * FROM customers ORDER BY {sort}"
    else:
        query = "SELECT * FROM customers"
    try:
        cur.execute(query)
        results = cur.fetchall()
    except:
        results = []
    cur.close()
    return jsonify({'customers': results})

@app.route('/api/v6/login', methods=['POST'])
def v6_login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    db = get_db()
    cur = db.cursor(cursor_factory=RealDictCursor)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cur.execute(query)
        results = cur.fetchall()
        if results:
            return jsonify({'success': True, 'user': results[0]})
    except:
        pass
    cur.close()
    return jsonify({'success': False}), 401

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)