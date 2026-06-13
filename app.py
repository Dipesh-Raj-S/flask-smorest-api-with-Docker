from flask import Flask,request
from db import items,stores
import uuid
from flask_smorest import abort

app=Flask(__name__)  #this creates a flask app, used to run the app and maintain end points

#stores will now look like
"""stores = {
    "abc123": {
        "id":"abc123",
        "name":"My Store"
    }
}          Now finding a store is easy: stores["abc123"] """


#Endpoint --> when our client requests data, we can return it
#flask route

@app.get("/store") # http://127.0.0.1:5000/store #"Hey Flask, if somebody sends a GET request to /store, run the function below."
def get_stores():
    return {"stores":list(stores.values())} #returning json data--> REST api always returns json data,
                            # here we receive status code of 200, ok

#how to create stores in our rest API --> we receive JSON from our client
#http://127.0.0.1:5000/store
#{
#	"name":"ice-cream-parlour"
#}
#-------------------------------------------------------------------------------------------------------------------------------
@app.post("/store")
def create_store():
    store_data=request.get_json() #store_data is a DICTIONARY with the json which is received(the json string is converted to a python dictionary)
    if "name" not in store_data:
        abort(400,message="bad request. ensure name is inlcluded inthe json payload")

    for store in stores.values():
        if store_data["name"]==store["name"]:
            abort(400,message="store already exists")    
    store_id=uuid.uuid4().hex
    store={**store_data, "id":store_id}
    stores[store_id]=store
    return store,201  ## here we receive status code of 201, ok, i have accepted the data and i will create

#Client sends:
"""{
    "name":"Ice Cream Shop"
}

{
    **store_data,
    "id":"abc123"
}
becomes:
{
    "name":"Ice Cream Shop",
    "id":"abc123"
}
"""

#WHY do we use database instead of a python list ?
#cuz python list doesnt persist between app runs, they just get deleted cuz they live in memory only, cuz of tht we use database

#----------------------------------------------------------------------------------------------------------------------------------

#client send data and we add it--> either by json payload or through the URL

#handling if the data comes through URL
#http://127.0.0.1:5000/store?name=My Store --> query string
#now ,here http://127.0.0.1:5000/store/My Store/item  -> json body
#{
#	"name":"ice-cream",
#	"price":22.99,
#    "store_id":"abc123"
#}

@app.post("/item")
def create_item():
    item_data=request.get_json()
    #if the client doesnt send any one of the particular field: error occurs and app crashes
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400,
              message="bad request. ensure 'price, 'store_id and 'name' are included in the the json payload.")

    #to avoid adding two items twice
    for item in items.values():
        if(item_data["name"]==item["name"] and item_data["store_id"]==item["store_id"]):
            abort(404,message="item alreay exist")


    if item_data["store_id"] not in stores:
        abort(404,message="Store not found")

    item_id=uuid.uuid4().hex
    item={**item_data,"id":item_id}
    items[item_id]=item

    return item, 201
    
#--------------------------------------------------------------------------------------------------------------------

##to get all the items
@app.get("/item")
def get_all_items():
    return {"items":list(items.values())}

#--------------------------------------------------------------------------------------------------------------------

#when client wants to get the store info
#http://127.0.0.1:5000/store/My Store    no need to send any json data
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,message="Store not found")

#--------------------------------------------------------------------------------------------------------------------

#when client wants to get items of a specific store
#http://127.0.0.1:5000/store/My Store/item    no need to send any json data

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message="item not found")
    
#-----------------------------------------------------------
#to delete an item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"item deleted."}
    except KeyError:
        abort(404, message="Item not found.")

#-----------------------------------------------------------
#updating items
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data=request.get_json()
    if("price" not in item_data or "name" not in item_data):
        abort(400,message="bad request. ensure 'price and 'name' are included in the the json payload.")
    try:
        item=items[item_id]
        item.update(item_data)   # or item |= item_data -->piping to update dictionary
        return item
    except KeyError:
        abort(404, message="item not found")

#----------------------------------------------------------------
#Deleting Stores
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"store deleted"}
    except KeyError:
        abort(404,message="store not found.")