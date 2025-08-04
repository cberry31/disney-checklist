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
        checklist_data[land] = land_data
        logging.debug(f"Updated {land} {attraction_id} to {land_data[attraction_id]['didRide']}")

    with open("./data/attractions.json", "w") as file:
        json.dump(checklist_data, file, indent=4)
        logging.debug(f"Updated {land} {attraction_id} to {land_data[attraction_id]['didRide']}")

    return Response("OK", status=200)

# TODO: Implement a way to update the file with an array of attractions


@app.route("/checklist", methods=["POST"])
def edit_checklist():
    data = json.loads(request.data)
    park = data["park"]
    checked = data["checked"]
    with open("data/attractions.json", "r+") as file:
        checklistData = json.load(file)
        checklistParkData = checklistData[park]
        for attraction in checklistParkData.keys():
            if checklistParkData[attraction]["didRide"] and attraction not in checked:
                checklistParkData[attraction]["didRide"] = False
            elif not checklistParkData[attraction]["didRide"] and attraction in checked:
                checklistParkData[attraction]["didRide"] = True
        checklistData[park] = checklistParkData
        file.write(checklistData)

@app.route("/test", methods=["POST"])
def test():
    data = json.loads(request.data)
    logging.debug(data)
    return Response("OK", status=200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
