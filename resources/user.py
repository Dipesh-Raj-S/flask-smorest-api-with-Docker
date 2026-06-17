from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token #When the user has the access token and sends us whenever a request is made from the client side, 
                                                    #we come to know that this user has once given his login, the username and password, and it was verified. 
                                                    #We can give access to certain endpoints. 

from db import db
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        try:
            user=UserModel(username=user_data["username"],
                           password=pbkdf2_sha256.hash(user_data["password"]))
            
            db.session.add(user)
            db.session.commit()

            return {"message":"user created successfully"},201

        except IntegrityError: # when it violates some condition that we have sent
            abort(400,message="A USERNAME with that name already exixts")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user=UserModel.query.filter(UserModel.username==user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):#we hash the user_data password and check whether the hashed password stored in database is same and verify it,, we dont unhash and check
            access_token=create_access_token(identity=str(user.id))
            return {"access_token":access_token} #the token is encoded, so it canbe decoded,
                                                 #only if it is hashed u cant unhash
                                                 #the user id is stored --> "sub"
                                                 #Anyone having this JWT access token can pretend to be this user and do all the activities. 
                                                 #We can also find which users this is and then can give only allowed permissions for that user. 
        abort(401,message="invalid credentials.")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200