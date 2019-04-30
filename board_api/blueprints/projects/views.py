# from flask import Blueprint, jsonify, request
# from models.project import Project
# from helpers import encode_auth_token, decode_auth_token
# from werkzeug.security import check_password_hash

# sessions_api_blueprint = Blueprint('sessions_api',
#                                 __name__,
#                                 template_folder='templates')

# @sessions_api_blueprint.route('/', methods=['POST'])
# def create():
#     post_data = request.get_json()
#     email = post_data['email']

#     user = User.get(User.email == email)

#     if user and check_password_hash(user.password, post_data['password']):
#         token = encode_auth_token(user)
#         user_data = {"id": user.id, "username": user.username, "email": user.email}
#         return jsonify(status="success", message=f"Successfully signed in as {user.username}", auth_token=token.decode(), user=user_data)
#     else:
#         return jsonify(status="failed", message="Passwords do not match.")