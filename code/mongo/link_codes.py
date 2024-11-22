from pymongo.database import Collection

class LinkCodesModel:

    def create_link_code_telegram(self, link_collection: Collection, chat_id: int, link_code: str):
        return link_collection.insert_one({"chat_id": chat_id, "link_code": link_code, "discord_id": 0})
    
    def create_link_code_discord(self, link_collection: Collection, discord_id: int, link_code: str):
        return link_collection.insert_one({"chat_id": 0, "link_code": link_code, "discord_id": discord_id})
    
    def fetch_link_code(self, link_collection: Collection, link_code: str):
        return link_collection.find_one({ "link_code": link_code})
    
    def fetch_link_code_telegram(self, link_collection: Collection, chat_id: int):
        return link_collection.find_one({"chat_id": chat_id})
    
    def fetch_link_code_discord(self, link_collection: Collection, discord_id: int):
        return link_collection.find_one({"discord_id": discord_id})
    
    def delete_link_code(self, link_collection: Collection, link_code: str):
        return link_collection.delete_one({"link_code": link_code})