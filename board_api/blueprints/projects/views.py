from flask import Blueprint, jsonify, request
from models.user import User
from models.client import Client
from models.project import Project
from helpers import encode_auth_token, decode_auth_token

projects_api_blueprint = Blueprint('projects_api',
                                  __name__,
                                  template_folder='templates')

#    name = pw.CharField()
#    type = pw.CharField()
#    client_id = pw.ForeignKeyField(Client, backref='projects')
#    date = pw.DateField()
#    currency = pw.CharField()
#    total = pw.DecimalField(decimal_places=2)

@projects_api_blueprint.route('/', methods=['POST'])
def create():
    post_data = request.get_json()
    name = post_data['name']
    project_type = post_data['project_type']
    country = post_data['country']
    country = post_data['country']
    country = post_data['country']
    country = post_data['country']

    client = Client(name=name, industry=industry, country=country)

    if client.save():
        client_data = {"id": client.id, "name": client.name,
                       "industry": client.industry, "country": client.country}
        return jsonify(status="success", message=f"Client {name} added.", client=client_data)
    else:
        return jsonify(status="failed", message=client.errors)


# @projects_api_blueprint.route('/list', methods=['GET'])
# def list_clients():
#     auth_header = request.headers.get('Authorization')

#     if auth_header:
#         token = auth_header.split(" ")[1]
#     else:
#         return jsonify(status="failed", message="No authorization header found.")

#     user_id = decode_auth_token(token)
#     user = User.get(User.id == int(user_id))

#     clients = Client.select()
#     client_data = [{
#         "id": int(c.id),
#         "name": c.name,
#         "industry": c.industry,
#         "country": c.country
#     } for c in clients]

#     if user:
#         return jsonify(client_data)
#     else:
#         return jsonify(status="failed", message="Authentication failed")

# # [D] - Delete client from database
# @projects_api_blueprint.route('/delete', methods=['POST'])
# def delete_client():
#     auth_header = request.headers.get('Authorization')

#     if auth_header:
#         token = auth_header.split(" ")[1]
#     else:
#         return jsonify(status="failed", message="No authorization header found.")

#     user_id = decode_auth_token(token)
#     user = User.get(User.id == int(user_id))

#     post_data = request.get_json()
#     id = post_data['id']

#     client = Client.get_or_none(Client.id == id)
#     delete = Client.delete().where(Client.id == id)

#     if not client:
#         return jsonify(status="failed", message="Could not find client in database.")
#     elif delete.execute():
#         return jsonify(status="success", message=f"{client.name} deleted.")
#     else:
#         return jsonify(status="failed", message=f"Unable to delete {client_name}")
