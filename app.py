import os
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from src.modules.courses.endpoints import api as course_api
from src.modules.quizzes.endpoints import api as quizz_api
from src.service_modules.db.conn import db
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_CONNECTION
app.config['API_TITLE'] = "Educational Platform API's"
app.config['API_VERSION'] = "v1"
app.config['OPENAPI_VERSION'] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = "/"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger"
app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

blplist = [course_api, quizz_api]
for blp in blplist:
    api.register_blueprint(blp)

def run_migrations():
    with app.app_context():
        os.system("flask db upgrade")

if __name__ == '__main__':
    run_migrations()
    app.run(host='0.0.0.0', port=5000, debug=True)