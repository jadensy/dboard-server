from flask import Blueprint, jsonify, make_response, request
from models.user import User
from werkzeug.security import generate_password_hash

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

# [C] - Create user
@users_api_blueprint.route('/', methods=['POST'])
def create():
    request_data = request.get_json()
    username = request_data['username']
    email = request_data['email']
    password_hash = generate_password_hash(request_data['password'])

    user = User(username=username, email=email, password=password_hash)
    if user.save():
        return jsonify(status="success", message=f"Account successfully created for {username}.")
        # add JWT
    else:
        errors = user.errors
        return jsonify(status="failed", message=errors)

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


