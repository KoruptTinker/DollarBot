from pymongo.database import Collection

class SpendsModel:

    def create_spend_from_telegram(self, spends_collection: Collection = None, chat_id: str = "", date: str = "", category:str = "", amount: int = 0):
        return spends_collection.insert_one({"user": chat_id, "date": date, "category": category, "amount": amount})

    def fetch_spends_from_telegram(self, spends_collection: Collection = None, chat_id: str = ""):
        return sorted(list(spends_collection.find({"user": chat_id})), key=lambda x: x["date"])