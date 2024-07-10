from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token
from models import User, Organisation



api_bp = Blueprint('api', __name__)


@api_bp.get('/users/<int:userId>')
def get_user(userId):
    try:
        user = User.query.get(userId)
        if user:
            user_dict = user.to_dict()
            response = {
                "status":"success",
                "message": "user record",
                "data": user_dict
            }
            return make_response(jsonify(response), 200)
        else:
            return make_response(jsonify(message="User not found"), 404)    
    except Exception as e:
            return make_response(jsonify(message="Error retrieving user"), 500)
    

@api_bp.get('/organisations')
def get_organisations():

    try:
        user_organisations = [organisation.to_dict() for organisation in Organisation.query.order_by(User.organisation).all()]
        response = {
            "status":"success",
            "message": "User Organisations",
            "data": {
                "organisations": user_organisations
            }
        }
        
        return make_response(jsonify(response), 200)
    except Exception as e:
        return make_response(jsonify(message="Error retrieving organisations"), 500)
    

@api_bp.get('/organisations/<int:orgId>')
def get_organisation(orgId):
    try:
        organisation = Organisation.query.filter_by(orgId=orgId).first()
        response = {
            "status":"success",
            "message": "User's Organisation",
            "data": {
                organisation
            }
        }
        
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        return make_response(jsonify(message="Error retrieving organisation"), 500)
    


@api_bp.post('/organisations')
def create_organisation():
    
    data = request.get_json()
    required_fields = ['name', 'description']
    if not all(field in data for field in required_fields):
        return jsonify(
            {
                "status": "Bad request",
                "message": "client error",
            }
        ), 400
    
    new_organisation = Organisation(
        name = data.get('name'),
        description = data.get('description'),
    )
    
    new_organisation.save()
    
    return make_response(jsonify(
        {
            "status": "success",
            "message": "Organisation crreated successfully",
            "data":{
                "orgId": new_organisation.orgId,
                "name": new_organisation.name,
                "description": new_organisation.description
            }   
        }
    ), 201)
        
@api_bp.post('/organisations/<int:orgId>')
def add_user_organisation(orgId):
    data = request.get_json()
    
    organisation = Organisation.organisation_by_orgId(orgId=orgId)
    user = User.get_user_by_userId(userId= data.get('userId'))
    if user is None:
        return jsonify(
            {
                "status": "Bad request",
                "message": "client error",
            }
        ), 400
        # organisation = Organisation.query.filter_by(orgId=orgId).first()
    
    new_user = User(
        userId = data.get("userId")
    )
    
    new_user.save()
    organisation.user.append(new_user)
    
    return jsonify(
            {
                "status": "success",
                "message": "User added to organisation successfully",
            }
        ), 200
    
        