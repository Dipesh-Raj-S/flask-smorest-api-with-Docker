from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint  #Load all routes from item.py
from resources.store import blp as StoreBlueprint  #Load all routes from store.py


app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True #It's a Flask configuration which says if there are any exceptions which occur, just propogate it to the main app.py. 
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

#http://localhost:5000/swagger-ui