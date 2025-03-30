from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import Response
from flask import url_for

from geo_activity_playground.webui.authenticator import Authenticator
from geo_activity_playground.webui.authenticator import needs_authentication
from geo_activity_playground.webui.explorer.controller import ExplorerController


def make_explorer_blueprint(
    explorer_controller: ExplorerController,
    authenticator: Authenticator,
) -> Blueprint:
    blueprint = Blueprint("explorer", __name__, template_folder="templates")

    @blueprint.route("/<zoom>")
    def map(zoom: str):
        return render_template(
            "explorer/index.html.j2", **explorer_controller.render(int(zoom))
        )

    @blueprint.route("/enable-zoom-level/<zoom>")
    @needs_authentication(authenticator)
    def enable_zoom_level(zoom: str):
        explorer_controller.enable_zoom_level(int(zoom))
        return redirect(url_for(".map", zoom=zoom))

    @blueprint.route("/<zoom>/<north>/<east>/<south>/<west>/explored.<suffix>")
    def download(zoom: str, north: str, east: str, south: str, west: str, suffix: str):
        mimetypes = {"geojson": "application/json", "gpx": "application/xml"}
        return Response(
            explorer_controller.export_explored_tiles(
                int(zoom),
                float(north),
                float(east),
                float(south),
                float(west),
                suffix,
            ),
            mimetype=mimetypes[suffix],
            headers={"Content-disposition": "attachment"},
        )

    @blueprint.route("/<zoom>/<north>/<east>/<south>/<west>/missing.<suffix>")
    def missing(zoom: str, north: str, east: str, south: str, west: str, suffix: str):
        mimetypes = {"geojson": "application/json", "gpx": "application/xml"}
        return Response(
            explorer_controller.export_missing_tiles(
                int(zoom),
                float(north),
                float(east),
                float(south),
                float(west),
                suffix,
            ),
            mimetype=mimetypes[suffix],
            headers={"Content-disposition": "attachment"},
        )

    return blueprint
