from flask import Blueprint, jsonify, request
from models.user import User
from models.client import Client
from models.project import Project
from helpers import encode_auth_token, decode_auth_token

projects_api_blueprint = Blueprint('projects_api',
                                  __name__,
                                  template_folder='templates')

@projects_api_blueprint.route('/', methods=['POST'])
def create():
    post_data = request.get_json()
    name = post_data['name']
    project_type = post_data['projectType']
    client_id = post_data['clientID']
    date = post_data['date']
    currency = post_data['currency']
    total = post_data['total']

    project = Project(name=name, project_type=project_type, client_id=client_id,
                date=date, currency=currency, total=total)

    if project.save():
        client = Client.get_by_id(client_id)

        client_data = { "id": int(client.id),
                        "name": client.name,
                        "industry": client.industry,
                        "country": client.country}

        project_data = {"id": project.id,
                        "name": project.name,
                        "project_type": project.project_type,
                        "client": client_data,
                        "date": str(project.date),
                        "currency": str(project.currency),
                        "total": project.total}

        return jsonify(status="success", message=f"Project added: {name}", project=project_data)
    else:
        return jsonify(status="failed", message="Failed to save new project.")

@projects_api_blueprint.route('/index', methods=['GET'])
def index():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        return jsonify(status="failed", message="No authorization header found.")

    user_id = decode_auth_token(token)
    user = User.get(User.id == int(user_id))

    projects = Project.select()

    project_data = [{
        "id": project.id,
        "name": project.name,
        "project_type": project.project_type,
        "client_name": Client.get_by_id(project.client_id).name,
        "date": str(project.date),
        "currency": project.currency,
        "total": str(project.total)} for project in projects]

    if user:
        return jsonify(project_data)
    else:
        return jsonify(status="failed", message="Authentication failed.")

@projects_api_blueprint.route('/<project_id>', methods=['GET'])
def show(project_id):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify(status="failed", message="No authorization header found.")
    else:
        token = auth_header.split(" ")[1]
        user_id = decode_auth_token(token)
        user = User.get(User.id == int(user_id))

        project = Project.get_by_id(project_id)

        project_data = {
            "id": project.id,
            "name": project.name,
            "project_type": project.project_type,
            "client_id": str(project.client_id),
            "client_name": Client.get_by_id(project.client_id).name,
            "date": str(project.date),
            "currency": project.currency,
            "total": str(project.total)}

        if user:
            return jsonify(project_data)
        else:
            return jsonify(status="failed", message="Authentication failed.")

@projects_api_blueprint.route('/<project_id>/update', methods=['PUT'])
def update(project_id):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify(status="failed", message="No authorization header found.")
    else:
        token = auth_header.split(" ")[1]
        user_id = decode_auth_token(token)
        user = User.get(User.id == int(user_id))
        put_data = request.get_json()

        project = Project.get_by_id(project_id)

        ## if key exists in JSON, then iterate (currently not working):
        # for k, v in put_data.items():
        #     project.k = v

        project.name = put_data['name']
        project.client_id = put_data['clientID']
        project.project_type = put_data['projectType']
        project.date = put_data['date']
        project.currency = put_data['currency']
        project.total = put_data['total']

        if project.save():
            return jsonify(status="success", message="Project details updated.")
        else:
            return jsonify(status="failed", message="Unable to update project details.")

@projects_api_blueprint.route('/<project_id>/delete', methods=['POST'])
def delete(project_id):
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify(status="failed", message="No authorization header found.")
    else:
        token = auth_header.split(" ")[1]
        user_id = decode_auth_token(token)
        user = User.get(User.id == int(user_id))
        if user:
            project = Project.get_or_none(Project.id == project_id)
            delete = Project.delete().where(Project.id == project_id)

            if not project:
                return jsonify(status="failed", message="Could not find project in database.")
            elif delete.execute():
                return jsonify(status="success", message="Project deleted.")
            else:
                return jsonify(status="failed", message="Unable to delete project.")
