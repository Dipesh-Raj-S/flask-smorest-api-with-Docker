import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema


#BLUEPRINT IN FLASK-SMOREST
#used to divide api into multiple segments

blp= Blueprint("stors",__name__,description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self,store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404,message="Store not found")

    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message":"store deleted"}
        except KeyError:
            abort(404,message="store not found.")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores":list(stores.values())} 
    
    @blp.arguments(StoreSchema)
    def post(self,store_data):
        
        for store in stores.values():
            if store_data["name"]==store["name"]:
                abort(400,message="store already exists")    
        store_id=uuid.uuid4().hex
        store={**store_data, "id":store_id}
        stores[store_id]=store
        return store,201  ## here we receive status code of 201, ok, i have accepted the data and i will create