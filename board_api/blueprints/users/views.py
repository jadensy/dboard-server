from flask import Blueprint, jsonify, request
from models.user import User
from helpers import encode_auth_token, decode_auth_token
from werkzeug.security import generate_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

# [C] - Create user
@users_api_blueprint.route('/', methods=['POST'])
def create():
    post_data = request.get_json()
    username = post_data['username']
    email = post_data['email']
    password_hash = generate_password_hash(post_data['password'])

    user = User(username=username, email=email, password=password_hash)

    if user.save():
        token = encode_auth_token(user)
        user_data = {"id": user.id, "username": user.username, "email": user.email}
        return jsonify(status="success", message=f"Account successfully created for {username}.", auth_token=token.decode(), user=user_data)
    else:
        return jsonify(status="failed", message=user.errors)

# [R] - Read user details
@users_api_blueprint.route('/me', methods=['GET'])
def show_user():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        return jsonify(status="failed", message="No authorization header found.")

    user_id = decode_auth_token(token)
    user = User.get(User.id == int(user_id))

    if user:
        return jsonify(id=str(user.id), username=user.username, email=user.email)
    else:
        return jsonify(status="failed", message="Authentication failed")

# [U] - Update user details
@users_api_blueprint.route('/me', methods=['PUT'])
def update_user():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        return jsonify(status="failed", message="No authorization header found.")

    user_id = decode_auth_token(token)
    user = User.get(User.id == int(user_id))
    put_data = request.get_json()

    if user:
        if "password" in put_data:
            user.password = generate_password_hash(put_data['password'])

        user.username = put_data['username']

        user_data = {"id": user.id, "username": user.username, "email": user.email}

        if user.save():
            return jsonify(status="success", message="Profile successfully updated.", user=user_data)
        else:
            return jsonify(status="failed", message=user.errors)