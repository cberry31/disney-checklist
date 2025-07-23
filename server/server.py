import json
import logging
import os

from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
stream_handler = logging.StreamHandler()
logging_level = os.environ.get("LOGGING_LEVEL", "INFO").upper()
logging.basicConfig(level=logging_level)
stream_handler.setLevel(logging_level)
app.logger.addHandler(stream_handler)


@app.route("/checklist", methods=["GET"])
def get_checklist():
    with open("./data/attractions.json", "r") as file:
        checklist_data = file.read()
        checklist_data = json.loads(checklist_data)
    return Response(json.dumps(checklist_data), status=200)


@app.route("/checklist/<land>", methods=["GET"])
def get_checklist_by_land(land):
    with open("./data/attractions.json", "r") as file:
        checklist_data = json.load(file)
        if land not in checklist_data:
            return Response("Land not found", status=404)
        land_data = checklist_data[land]
    return Response(json.dumps(land_data), status=200)


@app.route("/checklist/<land>/<attraction_id>", methods=["PUT"])
def update_checklist(land, attraction_id):
    with open("./data/attractions.json", "r+") as file:
        checklist_data = json.load(file)
        land_data = checklist_data.get(land, {})
        if attraction_id not in land_data:
            return Response("ID not found", status=404)

        didRide = land_data.get(attraction_id, {}).get("didRide", False)
        land_data[attraction_id]["didRide"] = not didRide

    with open("./data/attractions.json", "w") as file:
        json.dump(checklist_data, file, indent=4)

    return Response("OK", status=200)


@app.route("/checklist", methods=["PUT"])
def edit_checklist():
    try:
        new_data: dict = json.loads(request.data)
        data: dict = {}
        with open("./data/attractions.json", "r") as file:
            data = json.load(file)

        if data is None or data == {}:
            return Response("Checklist not found", status=404)

        for land in new_data.keys():
            if land not in data:
                raise ValueError(f"Land '{land}' not found in checklist data")
            for attraction in new_data[land]:
                attraction_id = attraction.get("id")
                if attraction_id in data[land]:
                    data[land][attraction_id]["didRide"] = attraction.get(
                        "didRide", False
                    )

        with open("./data/attractions.json", "w") as file:
            json.dump(data, file, indent=4)
        return Response("Checklist updated successfully", status=200)

    except json.JSONDecodeError:
        return Response("Invalid JSON format", status=400)
    except Exception as e:
        logging.error(f"Error updating checklist: {e}")
        return Response(str(e), status=500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
