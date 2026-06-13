from marshmallow import Schema, fields

#in this we define how the input,output behaves
#ItemSchema = Rules for an Item

class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

"""
this is checking the payload coming in (json format) 
✅ name exists
✅ name is string

✅ price exists
✅ price is float

✅ store_id exists
✅ store_id is string

id        -> dump_only=True -->Client cannot send id. Server sends id.
"""
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)