from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

# Blueprints
from .routes.health import blp as root_blp
from .routes.notes import blp as notes_blp


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask app with CORS and API docs."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # CORS enabled for all routes and origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # OpenAPI / Swagger UI config
    app.config["API_TITLE"] = "Simple Notes API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.register_blueprint(root_blp)
    api.register_blueprint(notes_blp)

    return app


# Expose app for run.py imports
app = create_app()
