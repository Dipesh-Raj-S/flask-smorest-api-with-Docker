from db import db

#any class that we create , it maps to a tabble with coloumns and sqlalchemy will automatically convert table rows to python objects

class ItemModel(db.Model):
    __tablename__="items" #Table name called items 

    #Defining all the IDs to be in the column 
    id=db.Column(db.Integer,primary_key=True)  #In Postgres, all this ID will be auto filled, like incremented one by one. 
    name=db.Column(db.String(80),unique=True,nullable=False)
    price=db.Column(db.Float(precision=2),unique=False,nullable=False)
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False,nullable=False) #This value we will be linking it with the other table, also store table. This ID should match the ones in the store table. 
                                                                # for doing this, we use ONE TO MANY RELATIONSHIPS
                                                                # many items can have same store id 
                                                                #store_id is a foreign key which is connecting this table to store.py
                                                                #db.Foreignkey("stores.id")--> stores is the next table's name-->__tablename__="stores"
                                                                #benefits of using foreign_key:
                                                                #1.You won't be able to create an item that has a store ID that doesn't have an equal value in the stores table,\
                                                                #because it wont be having appropriate store to link with it
    store=db.relationship("StoreModel",back_populates="items") #The SQLAlchemy knows that the stores table is used by the Storemodel class. 
                                                                #in notes.txt

    tags=db.relationship("TagModel",back_populates="items",secondary="items_tags")