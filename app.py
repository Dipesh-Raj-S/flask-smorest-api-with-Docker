from flask import Flask
from flask_smorest import Api

import os
from db import db
import models #this automatically imports StoreModel,ItemModel

from resources.item import blp as ItemBlueprint  #Load all routes from item.py
from resources.store import blp as StoreBlueprint  #Load all routes from store.py


def create_app(db_url=None):
    app = Flask(__name__)

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
    db.init_app(app)  #Connect Flask with SQLAlchemy.

    api = Api(app)  

    @app.before_request
    def create_tables():
        db.create_all()



    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)  

    return app

#http://localhost:5000/swagger-ui