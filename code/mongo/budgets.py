from pymongo.database import Collection

class BudgetsModel:

    def create_budget_from_telegram(self, budgets_collection: Collection = None, chat_id: str = ""):
        return budgets_collection.insert_one({"user": chat_id, "category": {}})
    
    def reset_budget_from_telegram(self, budgets_collection: Collection = None, chat_id: str = ""):
        return budgets_collection.update_one({"user": chat_id}, {"$set": {f"category": {}}})
    
    def fetch_budget_from_telegram(self, budgets_collection: Collection = None, chat_id: str = ""):
        return budgets_collection.find_one({"user": chat_id})

    def update_budget_category(self, budgets_collection: Collection = None, chat_id: str = "", category:str = "", amount: float = 0):
        return budgets_collection.update_one({"user": chat_id}, {"$set": {f"category.{category}": amount}})