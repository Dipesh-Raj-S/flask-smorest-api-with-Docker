import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema,ItemUpdateSchema

from sqlalchemy.exc import SQLAlchemyError

from  db import db
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200,ItemSchema)  #mainly for responses from our server
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data,item_id):
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            item |= item_data

            return item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):  #item_data is the validated data which the schema requested
        item=ItemModel(**item_data)

        try:
            db.session.add(item) #keep many things  ready
            db.session.commit()  #commit all the data to the db, if some problem while adding, u can do rollback,which makes Make sure that the session remains consistent and remains usable. 
        except SQLAlchemyError:
            abort(500,message="an error occured while inserting the item")

        return item