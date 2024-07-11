from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from models import User, Organisation
from schemas import UserSchema


api_bp = Blueprint('api', __name__)

@api_bp.get("/")
def home():
    return "Stage Two - Kindly Login/Register an account!", 200

@api_bp.get('/users/all')
def get_all_users():
    page = request.args.get('page', default=1, type=int)
    
    per_page = request.args.get('per_page', default=3, type=int)
    
    users = User.query.paginate(
        page= page,
        per_page= per_page
    )
    
    result = UserSchema().dump(users, many=True)
    return jsonify(
        {
            "users": result
        }
    ), 200

@api_bp.get('/users/<int:userId>')
@jwt_required()
def get_user(userId):
    try:
        user = User.user_by_userId(userId = userId)
        if user is not None:
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
        
@api_bp.patch('/organisations/<int:orgId>')
@jwt_required()
def add_user_organisation(orgId):
    data = request.get_json()
    
    organisation = Organisation.organisation_by_orgId(orgId==orgId)
    user = User.user_by_userId(userId= data.get('userId'))
    if user is not None:
        # organisation = Organisation.query.filter_by(Organisation.orgId=orgId).first()
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
    
    return jsonify(
            {
                "status": "Bad request",
                "message": "client error",
            }
        ), 400   