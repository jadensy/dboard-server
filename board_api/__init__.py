from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from board_api.blueprints.users.views import users_api_blueprint
from board_api.blueprints.sessions.views import sessions_api_blueprint
from board_api.blueprints.clients.views import clients_api_blueprint
# from board_api.blueprints.projects.views import projects_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/sessions')
app.register_blueprint(clients_api_blueprint, url_prefix='/api/v1/clients')
# app.register_blueprint(projects_api_blueprint, url_prefix='/api/v1/projects')

