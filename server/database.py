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
        attractions = self.collection.find(query)
        return attractions

    def toggleAttractionByID(self, park: str, id: str):
        query = {"park": park, "id": id}
        update = [{"$set": {"didRide": {"$not": "$didRide"}}}]
        self.collection.update_one(query, update)
