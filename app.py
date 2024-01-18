from flask import Flask, request
from flask_smorest import abort
import uuid
from db import stores, items

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "item": [
            {
                "name": "Chair",
                "price": 15.99

            }
        ]
    }
]

@app.get("/store")
def get_stores():
    """Request Stores Data"""
    return { "stores": list(stores.values()) }


@app.post("/store")
def create_stores():
    """Create Store Data"""
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = { **store_data, "id": store_id }
    stores[store_id] = store
    return store, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    """Request Store Data"""
    try:
        return stores[store_id], 201
    except KeyError:
        return { "message": "Store not found" }, 404


@app.get("/store/<string:name>/item")
def get_store_item(name):
    """Get Store Item"""
    _store = next((store for store in stores if store['name'] == name), None)
    if _store is not None:
        return { "items": _store["item"] }
    
    return { "message": "Store not found" }, 404


@app.get("/item")
def get_all_items():
    """GEt full item"""
    return { "items": list(items.values()) }


@app.get("/item/<string:item_id>")
def get_item(item_id):
    """GEt item by id"""
    try:
        return items[item_id]
    except KeyError:
        return { "message": "Item not found" }, 404
    

@app.post("/item")
def create_item(name):
    """Add Store Item"""
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return { "message": "Store not found" }, 404
    
    _item_id = uuid.uuid4().hex
    item = { **item_data, "id": _item_id}
    items[_item_id] = item
    
    return item, 201
