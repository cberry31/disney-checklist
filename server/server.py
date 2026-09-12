import json
import logging
import os

from flask import Flask, Response
from flask_cors import CORS

from database import AttractionRepository

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
stream_handler = logging.StreamHandler()
logging_level = os.environ.get("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=logging_level)
stream_handler.setLevel(logging_level)
app.logger.addHandler(stream_handler)

HEADERS = {"ngrok-skip-browser-warning": "true"}


@app.route("/checklist/<land>", methods=["GET"])
def get_checklist_by_land(land):
    attractionRepository = AttractionRepository()
    land_data = attractionRepository.getAttractionsByPark(land)
    return Response(json.dumps(land_data), status=200, headers=HEADERS)


@app.route("/checklist/<land>/<attraction_id>", methods=["PUT"])
def toggle_checklist_item(land, attraction_id):
    attractionRepository = AttractionRepository()
    attractionRepository.toggleAttractionByID(land, attraction_id)
    return Response("OK", status=200, headers=HEADERS)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
