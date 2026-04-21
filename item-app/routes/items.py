from flask import Blueprint, jsonify, request
from db import get_db
from models.item import Item

route = Blueprint('api', __name__, url_prefix='/api')

@route.get('/items')
def getItems():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, name FROM items")
    rows = cur.fetchall()
    print(rows)

    if len(rows) == 0:
        return jsonify({'error': 'Items not Found'})
    return jsonify([{"id": r["id"], "name": r["name"]} for r in rows])

@route.get('/item')
def getItem():
    id = request.args.get('id')
    db = get_db()
    cur = db.cursor()

    query = f"SELECT id, name FROM items WHERE id = {id}"
    cur.execute(query)
    
    item = cur.fetchone()
    if item == None:
        return jsonify({'error': 'Item not Found'})
    return jsonify(dict(item))

@route.post('/item')
def createItem():
    db = get_db()
    cur = db.cursor()

    data = request.get_json()
    name = data["name"]

    cur.execute("INSERT INTO items (name) VALUES (?)", (name,))
    db.commit()

    return jsonify({'id': cur.lastrowid, "name": name})

@route.put("/item/<int:id>")
def updateItem(id):
    db = get_db()
    cur = db.cursor()

    data = request.get_json()
    name = data["name"]

    cur.execute("UPDATE items SET name = ? WHERE id = ?", (name, id))
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Item not found"})

    return jsonify({"id": id, "name": name})

@route.delete("/item/<int:id>")
def deleteItem(id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM items WHERE id = ?", (id,))
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Item not found"})

    return jsonify({"status": "deleted", "id": id})

@route.get('/sensitive_data')
def sensitive_data():
    return jsonify({
        'user': 'admin',
        'password': 'password1234'
    })
        
