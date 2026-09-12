import os

from pymongo import MongoClient


class AttractionRepository:
    def __init__(self) -> None:
        uri = os.environ.get("MONGO_DB_URI")
        self.client = MongoClient(uri)
        database = self.client.get_database("disney-checklist")
        self.collection = database.get_collection("attractions")

    def getAttractionsByPark(self, park: str):
        query = {"park": park}
        cursor = self.collection.find(query)
        attractions = []
        for item in cursor:
            print(item)
            attractions.append({
                "id": item["id"],
                "park": item["park"],
                "land": item["land"],
                "didRide": item["didRide"],
                "name": item["name"]
                })
        return attractions

    def toggleAttractionByID(self, park: str, id: str):
        query = {"park": park, "id": id}
        update = [{"$set": {"didRide": {"$not": "$didRide"}}}]
        self.collection.update_one(query, update)
