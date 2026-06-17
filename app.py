from flask import Flask,jsonify
from flask_smorest import Api

from flask_jwt_extended import JWTManager
import secrets
import os
from db import db
import models #this automatically imports StoreModel,ItemModel

from resources.item import blp as ItemBlueprint  #Load all routes from item.py
from resources.store import blp as StoreBlueprint  #Load all routes from store.py
from resources.tag import blp as TagBlueprint     #Load all routes from tag.py
from resources.user import blp as UserBlueprint     #Load all routes from tag.py



def create_app(db_url=None):
    app = Flask(__name__)   #creates the server

    app.config["PROPAGATE_EXCEPTIONS"] = True #It's a Flask configuration which says if there are any exceptions which occur, just propogate it to the main app.py. 
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  

    #configuring db
    app.config["SQLALCHEMY_DATABASE_URI"]=db_url or os.getenv("DATABASE_URL","sqlite:///data.db") #this creates data.db and stores all the data, sqlite is fast
                                            #Which database should I use?
                                            #If no database is provided:sqlite:///data.db--> meaning create new file data.db and use it as database
                                            
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)  #Connect Flask with SQLAlchemy.  SQLite = Database Engine;;SQLAlchemy = ORM (Object Relational Mapper)

    api = Api(app)  
    
    app.config["JWT_SECRET_KEY"]="80281428440095199159231244525482792435"  #these are used for signing the JWTs.This is not the same as encryption. But rather, the JWT is used with the secret keySo that when a user sends us back a JWT to tell who they are, our app can 
                                        #Check the secret key and use it to verify that this app generated that JWT and therefore the JWT is valid. 
                                        #The flow goes like this:1. Client sends token
                                        #2. Server receives token
                                        #3. Server uses JOOS
                                        #4. Verifies signature
                                        #5. If valid, token was created by me
                                        #6. If invalid, someone has modified the token                                      
                                        #7. Reject request---> its like a shops stamp--> prevent jwt tampering
    jwt=JWTManager(app)


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )


    @app.before_request
    def create_tables():
        db.create_all()
    
    """
    Before EVERY HTTP request, run create_tables()--> 
    db.create_all() do?
SQLAlchemy looks at all your models:

class StoreModel(db.Model),class ItemModel(db.Model),class TagModel(db.Model),class ItemTags(db.Model)
and asks:
Do the corresponding tables exist?
If not:
CREATE TABLE stores ...,CREATE TABLE items ...,CREATE TABLE tags ...,CREATE TABLE items_tags ..."""

    api.register_blueprint(ItemBlueprint) #load all routes from item.py
    api.register_blueprint(StoreBlueprint)  #load all routes from store.py
    api.register_blueprint(TagBlueprint)  #load all routes from tag.py
    api.register_blueprint(UserBlueprint)  #load all routes from user.py

    """After registration:  these were seperate before
app.py
   │
   ├── item routes
   ├── store routes
   └── tag routes"""

    
    return app

#http://localhost:5000/swagger-ui