import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema

from db import db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from models import StoreModel

#BLUEPRINT IN FLASK-SMOREST
#used to divide api into multiple segments

blp= Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
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
    @blp.response(201,StoreSchema(many=True))
    def get(self):
        return {"stores":list(stores.values())} 
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema())
    def post(self,store_data):
        
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError: # when it violates some condition that we have sent
            abort(400,message="A Store with that name already exixts")

        except SQLAlchemyError:
            abort(500,message="An error occured creating the store.")
            return store