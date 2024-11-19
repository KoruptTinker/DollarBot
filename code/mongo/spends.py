from pymongo.database import Collection

class SpendsModel:

    def create_spend_from_telegram(self, spends_collection: Collection = None, chat_id: str = "", date: str = "", category:str = "", amount: int = 0):
        return spends_collection.insert_one({"user": chat_id, "date": date, "category": category, "amount": amount})

    def fetch_spends_from_telegram(self, spends_collection: Collection = None, chat_id: str = ""):
        return sorted(list(spends_collection.find({"user": chat_id})), key=lambda x: x["date"])
    
    def reset_spend_history_from_telegram(self, spends_collection: Collection = None, chat_id: str = ""):
        return spends_collection.delete_many({"user": chat_id})
    
    def delete_spend_history_from_telegram(self, spends_collection: Collection = None, chat_id: str = "", date: str = ""):
        return spends_collection.delete_many({"user": chat_id, "date": date})
    
    def update_spend_date_from_telegram(self, spends_collection: Collection = None, spend_id: str = "", date: str = ""):
        return spends_collection.update_one({"_id": spend_id}, {"$set": {"date": date}})

    def update_spend_category_from_telegram(self, spends_collection: Collection = None, spend_id: str = "", category: str = ""):
        return spends_collection.update_one({"_id": spend_id}, {"$set": {"category": category}})

    def update_spend_amount_from_telegram(self, spends_collection: Collection = None, spend_id: str = "", amount: int = 0):
        return spends_collection.update_one({"_id": spend_id}, {"$set": {"amount": amount}})