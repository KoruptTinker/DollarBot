import certifi
from pymongo import MongoClient
from .user import UsersModel
from .spends import SpendsModel
from .budgets import BudgetsModel
from typing import Optional
import atexit

class MongoDB:
    _connection_url = None
    _db = None
    _instance = None
    _users: UsersModel = None
    _spends: SpendsModel = None
    _budgets: BudgetsModel = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls, connection_url: str = "", db_name: str = ""):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._db = db_name
            cls._instance._connection_url = connection_url
            cls._instance._users = UsersModel()
            cls._instance._spends = SpendsModel()
            cls._instance._budgets = BudgetsModel()
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        """Establish MongoDB connection"""
        if not self._client:
            try:
                self._client = MongoClient(self._connection_url, tlsCAFile=certifi.where())
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

    def create_user_from_telegram(self, chat_id: str = ""):
        if chat_id:
            self._users.create_user_from_telegram(self._user_collection, chat_id)
            return True
        return False
    
    @property
    def _spends_collection(self):
        """Get reference to the spends collection in the DB"""
        return self._client.DollarBot.spends
    
    def create_spends_from_telegram(self, chat_id: str = "", date: str = "", category: str = "", amount: int = 0):
        if date and category and amount and chat_id:
            self._spends.create_spend_from_telegram(self._spends_collection, chat_id, date, category, amount)
            return True
    
        return False

    def fetch_spends_from_telegram(self, chat_id: str = ""):
        if chat_id:
            return self._spends.fetch_spends_from_telegram(self._spends_collection, chat_id)
    
        return []
    
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
            return self._budgets.fetch_budget_from_telegram(self._budgets_collection, chat_id)
    
        return None

    def update_budget_from_telegram(self, chat_id: str = "", category: str = "", amount: float = 0):
        if chat_id and category:
            self._budgets.update_budget_category(self._budgets_collection, chat_id, category, amount)
            return True
    
        return False
    
    def reset_budget_from_telegram(self, chat_id: str = ""):
        if chat_id:
            self._budgets.reset_budget_from_telegram(self._budgets_collection, chat_id)
            return True
    
        return False

    def close(self):
        """Manually close the connection"""
        self._cleanup()