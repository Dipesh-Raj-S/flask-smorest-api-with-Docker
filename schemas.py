from marshmallow import Schema, fields

#in this we define how the input,output behaves
#ItemSchema = Rules for an Item

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
   

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


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str()

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id=fields.Int()

class ItemSchema(PlainItemSchema):
    store_id=fields.Int(required=True,load_only=True) #Client sends it.Server doesn't return it.
    store=fields.Nested(PlainStoreSchema(),dump_only=True) #Inside Item,embed a Store.
    """
    Response becomes
    {
    "id":1,
    "name":"Milk",
    "price":20,

    "store":{
        "id":5,
        "name":"Reliance"
    }
}"""

class StoreSchema(PlainStoreSchema):
    items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    tags=fields.List(fields.Nested(PlainTagSchema()),dump_only=True)

class TagSchema(PlainTagSchema):
    store_id=fields.Int(load_only=True) #Client sends it.Server doesn't return it.
    store=fields.Nested(PlainStoreSchema(),dump_only=True) #Inside Item,embed a Store.



# PlainItemSchema and PlainStoreSchema contain only basic fields.

# ItemSchema extends PlainItemSchema and adds:
# - store_id (used when creating items)
# - nested store information

# StoreSchema extends PlainStoreSchema and adds:
# - list of items belonging to the store

# load_only=True
# -> Client can send field.
# -> API won't return field.

# dump_only=True
# -> API can return field.
# -> Client cannot send field.

# fields.Nested(...)
# -> Embed one object inside another.

# fields.List(fields.Nested(...))
# -> Embed a list of objects.

# Example:
# item.store
# becomes nested JSON store data

# store.items
# becomes a list of nested item data

