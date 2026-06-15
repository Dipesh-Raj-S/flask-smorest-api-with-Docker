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
        item=ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item=ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Deleting an item is not implemented")



    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self, item_data,item_id): # we handle an Idempotent request->Running one or ten requests should result in the same state of it by the end. 
        #AIM -> if the item exists, u update or else u create the item with all the properties included

        item=ItemModel.query.get(item_id)
        if item:
            item.price=item_data["price"]
            item.name=item_data["name"]
                
        else:
            item=ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

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