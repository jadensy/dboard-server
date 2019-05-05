from flask import Blueprint, jsonify, request
from models.user import User
from models.client import Client
from models.project import Project
from helpers import encode_auth_token, decode_auth_token
from peewee import fn

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
        currency_types = {}
        project_types = {}
        currency_revenue = {}
        project_revenue = {}

        currencies = Project.select(Project.currency.distinct())
        pr_type_count = Project.select(Project.project_type.distinct())
        countries = len(list(Client.select(Client.country.distinct())))

        for c in currencies:
            count = Project.select().where(Project.currency == c.currency).count()
            cr = {c.currency: count}
            currency_types.update(cr)

            revenue = Project.select(Project.total).where(Project.currency == c.currency)
            crt = []
            for r in revenue:
                crt.append(r.total)
                c_total = { c.currency: str(sum(crt)) }
                currency_revenue.update(c_total)

        for t in pr_type_count:
            count = Project.select().where(Project.project_type == t.project_type).count()
            pt = {t.project_type: count}
            project_types.update(pt)

            revenue = Project.select(Project.total).where(Project.project_type == t.project_type)
            prt = []
            for r in revenue:
                prt.append(r.total)
                t_total = { t.project_type: str(sum(prt)) }
                project_revenue.update(t_total)

        db_basic_data = {
            "project_count": project_count,
            "client_count": client_count,
            "countries": countries,
            "currency_types": currency_types,
            "project_types": project_types,
            "currency_revenue": currency_revenue,
            "project_revenue": project_revenue,
        }

        return jsonify(db_basic_data)
    else:
        return jsonify(status="failed", message="Authentication failed")
