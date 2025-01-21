from flask import Blueprint, request
from . import db
from .models import User
from .views import create_user_response, user_list_view, error_response

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    try:
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return create_user_response('User created successfully', 201)
    
    except Exception as e:
        return error_response(f"Error: {str(e)}", 400)

@user_controller.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return user_list_view(users)

@user_controller.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    
    try:
        user = User.query.get(id)
        if not user:
            return error_response('User not found', 404)
        
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)

        db.session.commit()
        return create_user_response('User updated successfully', 200)

    except Exception as e:
        return error_response(f"Error: {str(e)}", 400)

@user_controller.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return error_response('User not found', 404)

        db.session.delete(user)
        db.session.commit()
        return create_user_response('User deleted successfully', 200)

    except Exception as e:
        return error_response(f"Error: {str(e)}", 400)
