from pymongo.database import Collection


class UsersModel:

    def get_user_from_telegram(
        self, user_collection: Collection = None, chat_id: str = ""
    ):
        return user_collection.find_one({"telegram_chat_id": chat_id})

    def create_user_from_telegram(
        self, user_collection: Collection = None, chat_id: str = ""
    ):
        return user_collection.insert_one(
            {"telegram_chat_id": chat_id, "discord_id": None}
        )

    def link_discord_to_telegram(
        self,
        user_collection: Collection = None,
        chat_id: str = "",
        discord_id: str = "",
    ):
        return user_collection.update_one(
            {"telegram_chat_id": chat_id}, {"$set": {"discord_id": discord_id}}
        )
