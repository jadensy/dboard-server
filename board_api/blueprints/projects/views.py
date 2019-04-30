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
                        "currency": project.currency,
                        "total": project.total}

        return jsonify(status="success", message=f"Project added: {name}", project=project_data)
    else:
        return jsonify(status="failed", message="Failed to save new project.")

@projects_api_blueprint.route('/index', methods=['POST'])
def index():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]