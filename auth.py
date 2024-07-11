from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User, Organisation
import json


auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register_user():
    
    data = request.get_json()
    
    required_fields = ['firstName', 'lastName', 'email', 'password', 'phone']
    if not all(field in data for field in required_fields):
    # validate = [e for e in required_fields]
    # if not validate in data:
        response = (
            {"errors" : 
                { 
                    "message": "Missing required fields"
                }
            })
        resp = json.dumps(response)
        return jsonify(resp), 401
    
    user = User.get_user_by_username(email= data.get('email'))
    access_token = create_access_token(identity=data.get('email'))
    if user is not None:
        return jsonify(
            {
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "error": "User already exists"
            }
        ), 400
    
    new_user = User(
        firstName = data.get('firstName'),
        lastName = data.get('lastName'),
        email = data.get('email'),
        phone = data.get('phone')
    )
    
    new_user.set_password(password= data.get('password'))
    new_user.save()
    org_name = Organisation(name = f"{new_user.firstName}'s Organisation")
    org_name.save()
    new_user.organisation = org_name
    
    return make_response(jsonify(
        {
            "status": "success",
            "message": "Registration successful",
            "data":{
                "accessToken": access_token,
                "user": {
                    "userId": new_user.userId,
                    "firstName": new_user.firstName,
                    "lastName": new_user.lastName,
                    "email": new_user.email,
                    "phone":new_user.phone
                }
            }
        }
    ), 201)

@auth_bp.post('/login')
def login_user():
    
    data = request.get_json()
    
    user = User.get_user_by_username(email= data.get('email'))
    
    
    if user and (user.check_password(password = data.get('password'))):
        access_token = create_access_token(identity=user.userId)
        refresh_token = create_refresh_token(identity=user.userId)
        
        
        return make_response(jsonify(
            {
                "status": "success",
                "message": "Logged successful",
                "data":{
                    "accessToken": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "userId": user.userId,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "email": user.email,
                        "phone":user.phone
                    }
                }   
            }
        ), 200)
        
    return jsonify(
        {
            "status": "Bad request",
            "message": "Authentication failed",
            "error": "Invalid username or password"
        }
    ), 401
    
    

