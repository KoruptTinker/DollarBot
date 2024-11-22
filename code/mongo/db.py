import certifi
from pymongo import MongoClient
from .user import UsersModel
from .spends import SpendsModel
from .budgets import BudgetsModel
from .link_codes import LinkCodesModel
from typing import Optional
import atexit


class MongoDB:
    _connection_url = None
    _db = None
    _instance = None
    _users: UsersModel = None
    _spends: SpendsModel = None
    _budgets: BudgetsModel = None
    _link_codes: LinkCodesModel = None
    _client: Optional[MongoClient] = None

    def __new__(cls, connection_url: str = "", db_name: str = ""):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._db = db_name
            cls._instance._connection_url = connection_url
            cls._instance._users = UsersModel()
            cls._instance._spends = SpendsModel()
            cls._instance._budgets = BudgetsModel()
            cls._instance._link_codes = LinkCodesModel()
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Establish MongoDB connection"""
        if not self._client:
            try:
                self._client = MongoClient(
                    self._connection_url, tlsCAFile=certifi.where()
                )
                atexit.register(self._cleanup)
            except Exception as e:
                raise Exception(f"Failed to connect to MongoDB: {e}")

    def _cleanup(self):
        """Cleanup method to close connection"""
        if self._client:
            self._client.close()
            self._client = None

    @property
    def client(self) -> MongoClient:
        """Get MongoDB client instance"""
        return self._client

    @property
    def db(self):
        """Get default database instance"""
        return self._client[self._db]

    @property
    def _user_collection(self):
        """Get reference to the user collection in the DB"""
        return self._client.DollarBot.users

    def fetch_user_from_telegram(self, chat_id: str = ""):
        return self._users.get_user_from_telegram(self._user_collection, chat_id)
    
    def fetch_user_from_discord(self, discord_id: str = ""):
        return self._users.get_user_from_discord(self._user_collection, discord_id)

    def create_user_from_telegram(self, chat_id: str = ""):
        if chat_id:
            self._users.create_user_from_telegram(self._user_collection, chat_id)
            return True
        return False

    def link_discord_to_telegram(self, chat_id: str = "", discord_id: str = ""):
        if chat_id and discord_id:
            self._users.link_discord_to_telegram(
                self._user_collection, chat_id, discord_id
            )
            return True
        return False

    @property
    def _spends_collection(self):
        """Get reference to the spends collection in the DB"""
        return self._client.DollarBot.spends

    def create_spends_from_telegram(
        self, chat_id: str = "", date: str = "", category: str = "", amount: int = 0
    ):
        if date and category and amount and chat_id:
            self._spends.create_spend_from_telegram(
                self._spends_collection, chat_id, date, category, amount
            )
            return True

        return False

    def fetch_spends_from_telegram(self, chat_id: str = ""):
        if chat_id:
            return self._spends.fetch_spends_from_telegram(
                self._spends_collection, chat_id
            )

        return []

    def reset_spends_from_telegram(self, chat_id: str = ""):
        if chat_id:
            self._spends.reset_spend_history_from_telegram(
                self._spends_collection, chat_id
            )
            return True

        return False

    def delete_spends_from_telegram(self, chat_id: str = "", date: str = ""):
        if chat_id and date:
            self._spends.delete_spend_history_from_telegram(
                self._spends_collection, chat_id, date
            )
            return True

        return False

    def update_spend_date_from_telegram(self, spend_id: str = "", date: str = ""):
        if spend_id and date:
            report = self._spends.update_spend_date_from_telegram(
                self._spends_collection, spend_id, date
            )
            return True

        return False

    def update_spend_category_from_telegram(
        self, spend_id: str = "", category: str = ""
    ):
        if spend_id and category:
            self._spends.update_spend_category_from_telegram(
                self._spends_collection, spend_id, category
            )
            return True

        return False

    def update_spend_amount_from_telegram(self, spend_id: str = "", amount: int = 0):
        if spend_id and amount:
            self._spends.update_spend_amount_from_telegram(
                self._spends_collection, spend_id, amount
            )
            return True

        return False

    @property
    def _budgets_collection(self):
        """Get reference to the spends collection in the DB"""
        return self._client.DollarBot.budgets

    def create_budget_from_telegram(self, chat_id: str = ""):
        if chat_id:
            self._budgets.create_budget_from_telegram(self._budgets_collection, chat_id)
            return True

        return False

    def fetch_budget_from_telegram(self, chat_id: str = ""):
        if chat_id:
            return self._budgets.fetch_budget_from_telegram(
                self._budgets_collection, chat_id
            )

        return None

    def update_budget_from_telegram(
        self, chat_id: str = "", category: str = "", amount: float = 0
    ):
        if chat_id and category:
            self._budgets.update_budget_category(
                self._budgets_collection, chat_id, category, amount
            )
            return True

        return False

    def reset_budget_from_telegram(self, chat_id: str = ""):
        if chat_id:
            report = self._budgets.reset_budget_from_telegram(
                self._budgets_collection, chat_id
            )
            return True

        return False

    @property
    def _link_codes_collection(self):
        """Get reference to the spends collection in the DB"""
        return self._client.DollarBot.link_codes

    def create_link_code_from_telegram(self, chat_id: int, link_code: str):
        if chat_id and link_code:
            self._link_codes.create_link_code_telegram(
                self._link_codes_collection, chat_id, link_code
            )
            return True

        return False

    def create_link_code_from_discord(self, discord_id: int, link_code: str):
        if discord_id and link_code:
            self._link_codes.create_link_code_discord(
                self._link_codes_collection, discord_id, link_code
            )
            return True

        return False

    def fetch_link_code(self, link_code: str):
        if link_code:
            return self._link_codes.fetch_link_code(
                self._link_codes_collection, link_code
            )

        return None

    def fetch_link_code_from_discord(self, discord_id: int):
        if discord_id:
            return self._link_codes.fetch_link_code_discord(
                self._link_codes_collection, discord_id
            )

        return None

    def fetch_link_code_from_telegram(self, chat_id: int):
        if chat_id:
            return self._link_codes.fetch_link_code_telegram(
                self._link_codes_collection, chat_id
            )

        return None

    def delete_link_code(self, link_code: str):
        if link_code:
            return self._link_codes.delete_link_code(
                self._link_codes_collection, link_code
            )

        return None

    def close(self):
        """Manually close the connection"""
        self._cleanup()
