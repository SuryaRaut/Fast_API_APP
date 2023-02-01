
import uuid
from os import abort
from urllib import request

from fastapi import FastAPI
from pydantic import BaseModel  # Added to handle post request

app = FastAPI()


class Items(BaseModel):
    pass


class Store(BaseModel):
    store_name: str


stores = {
    "3045ede37f9d4ba988de644a697d55a1": {
        "store_id": "3045ede37f9d4ba988de644a697d55a1",
        "store_name": "store_1",
        "items": []
    }
}
items = []


@app.get('/')
def welcomeNote():
    return {"Welcome": "Welcome to Our Grocery App"}
    # return "Hello"


@app.post('/addStore')  # http://127.0.0.1:8000/addStore
def create_store(request: Store):
    curr_store = dict()
    store_id = uuid.uuid4().hex

    curr_store['store_id'] = store_id
    curr_store['store_name'] = request.store_name
    curr_store['items'] = []
    stores[store_id] = curr_store

    return curr_store


@app.get('/stores')  # http://127.0.0.1:8000/stores
def getallstores():
    return stores


@app.get('/store/<string:store_id>')  # http://127.0.0.1:8000/store/store_id
def getStore(store_id: str):
    try:
        return stores[store_id], 200
    except KeyError as e:
        return {"Error": f"Store not Found, Exception = {e}"}, 404


@app.delete('/store/<string:store_id>')  # http://127.0.0.1:8000/store/store_id
def deletestore(store_id):
    try:
        op = stores.pop(store_id)
        return op, 202
    except KeyError as e:
        abort(404, message=f"Store not Found having store_id = {store_id}")


@app.put('/store/<string:store_id>')  # http://127.0.0.1:8000/item/item_id
def putStore(store_id):
    put_store_data = request.get_json()

    if store_id not in stores:
        abort(404, message=f"Item not Found having store_id = {store_id}")

    if "store_name" not in put_store_data:
        abort(404, message=f"API does not have required parameters")

    stores[store_id]["store_name"] = put_store_data["store_name"]

    return stores[store_id], 202


@app.post('/addItem')  # http://127.0.0.1:8000/addItem
def addItem():
    item_data = request.get_json()
    print(f"item_data = {item_data}")

    if (("store_id" not in item_data)
            and ("item_name" not in item_data)
            and ("item_price" not in item_data)):
        abort(404, message=f"API does not have required parameters")

    if item_data["store_id"] not in stores:
        # return { "Error" : f"Store not found having store_id : { item_data['store_id'] }" }
        abort(404, message=f"Store not found having store_id : {item_data['store_id']}")

    for each_item in items.values():
        if ((each_item["store_id"] == item_data["store_id"])
                and (each_item["item_name"] == item_data["item_name"])):
            abort(404, message=f"Duplicate Item present in store_id : {item_data['store_id']}")

    item_id = uuid.uuid4().hex
    item_data["item_id"] = item_id

    items[item_id] = item_data

    return item_data, 201


@app.get('/items')  # http://127.0.0.1:8000/items
def getallitems():
    return items, 200


@app.get('/item/<string:item_id>')  # http://127.0.0.1:8000/item/item_id
def getitem(item_id):
    try:
        return items[item_id], 200
    except KeyError as e:
        abort(404, message=f"Item not Found, Exception = {e}")


@app.delete('/item/<string:item_id>')  # http://127.0.0.1:8000/item/item_id
def deleteitem(item_id):
    try:
        op = items.pop(item_id)
        return op, 202
    except KeyError as e:
        abort(404, message=f"Item not Found having item_id = {item_id}")


@app.put('/item/<string:item_id>')  # http://127.0.0.1:8000/item/item_id
def putItem(item_id):
    put_item_data = request.get_json()

    if item_id not in items:
        abort(404, message=f"Item not Found having item_id = {item_id}")

    if ("item_name" not in put_item_data) and ("item_price" not in put_item_data):
        abort(404, message=f"API does not have required parameters")

    items[item_id]["item_name"] = put_item_data["item_name"]
    items[item_id]["item_price"] = put_item_data["item_price"]

    if "store_id" in put_item_data:
        items[item_id]["store_id"] = put_item_data["store_id"]

    return items[item_id], 202

