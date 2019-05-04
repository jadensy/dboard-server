from flask import Blueprint, jsonify, request
from models.user import User
from models.client import Client
from models.project import Project
from helpers import encode_auth_token, decode_auth_token

dashboard_api_blueprint = Blueprint('dashboard_api',
                                  __name__,
                                  template_folder='templates')

@dashboard_api_blueprint.route('/', methods=['GET'])
def index():
    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        return jsonify(status="failed", message="No authorization header found.")

    user_id = decode_auth_token(token)
    user = User.get(User.id == int(user_id))

    if user:
        project_count = Project.select().count()
        client_count = Client.select().count()
        currency_revenue = {}
        project_revenue = {}

        currencies = Project.select(Project.currency.distinct())
        project_types = Project.select(Project.project_type.distinct())
        countries = Client.select(Client.country.distinct()).count()

        for c in currencies:
            count = Project.select().where(Project.currency == c.currency).count()
            cr = {c.currency: count}
            currency_revenue.update(cr)

        for t in project_types:
            count = Project.select().where(Project.project_type == t.project_type).count()
            pt = {t.project_type: count}
            project_revenue.update(pt)

        db_basic_data = {
            "project_count": project_count,
            "client_count": client_count,
            "countries": countries,
            "currency_revenue": currency_revenue,
            "project_revenue": project_revenue,
        }

        return jsonify(db_basic_data)
    else:
        return jsonify(status="failed", message="Authentication failed")
