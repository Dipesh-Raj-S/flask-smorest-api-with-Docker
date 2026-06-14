from db import db

class StoreModel(db.Model):
    __tablename__="stores"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    items=db.relationship("ItemModel",back_populates="store",lazy="dynamic") #in notes.txt
                                                                            #without lazy dynamic-> All data comes from DB immediately.
                                                                            #when we use it ,SQLAlchemy does NOT fetch items yet.Instead it returns a query object.
                                                                            #"Here is a query.Tell me what you want to do with it."
                                                                            #now u can get all items, or get only expensive ones..
                                                                        