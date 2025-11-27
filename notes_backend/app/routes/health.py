from flask_smorest import Blueprint
from flask.views import MethodView

# Root-level blueprint for info and health endpoints
blp = Blueprint("Root and Health", "root", url_prefix="/", description="Root info and health endpoints")


@blp.route("/")
class RootInfo(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """Basic API info route."""
        return {
            "name": "Simple Notes API",
            "version": "v1",
            "endpoints": {
                "health": "/health",
                "notes_collection": "/notes",
                "notes_item": "/notes/<id>",
                "docs": "/docs",
                "openapi": "/openapi.json",
            },
        }, 200


@blp.route("/health")
class HealthCheck(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """Healthcheck endpoint returning a simple OK signal."""
        return {"status": "ok"}, 200
