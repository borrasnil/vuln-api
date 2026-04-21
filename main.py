from flask import Flask, Blueprint, jsonify, request
from dataclasses import dataclass

next_id = 0
@dataclass
class Item:
    id: int
    name: str


app = Flask(__name__);
route = Blueprint('api', __name__, url_prefix='/api')

items: list[Item] = []

@route.get('/items')
def getItems():
    if len(items) == 0:
        return jsonify({'error': 'Items not Found'})
    return jsonify(items)

@route.get('/item/<int:id>')
def getItem(id):
    for item in items:
        if item.id != id: continue
        return jsonify(item)
    return jsonify({'error': 'Item not Found'})

@route.post('/item')
def createItem():
    try:
        data = request.get_json()
        name = data["name"]
        global next_id

        item = Item(id=next_id, name=name)
        items.append(item)
        next_id += 1

        return jsonify(item)
    except Exception as e:
        return jsonify({'error': str(e)})

@route.put('/item/<int:id>')
def updateItem(id):
    try:
        for item in items:
            if item.id != id: continue
            data = request.get_json()
            name = data["name"]
            items.remove(item)
            items.insert(id, Item(id, name))
            return jsonify(items[id])
        return jsonify({'error': 'Item not Found'})
    except Exception as e:
        return jsonify({'error': str(e)})


@route.delete('/item/<int:id>')
def deleteItem(id):
    for item in items:
        if item.id != id: continue
        # items.pop(id)
        return jsonify(item)
    return jsonify({'error': 'Item not Found'})


@route.get('/sensitive_data')
def sensitive_data():
    return jsonify({
        'user': 'admin',
        'password': 'password1234'
    })
        

app.register_blueprint(route)
if __name__ == "__main__":
    app.run(debug=True, port=3001)
   

