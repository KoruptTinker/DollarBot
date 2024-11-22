from dotenv import load_dotenv
import os
from typing import Optional


class Secrets:
    _instance: Optional["Secrets"] = None
    MongoConnectionURL: str = ""
    DBName: str = ""

    TelegramAPIKey: str = ""

    BotToken: str = ""
    GuildID: str = ""

    def __new__(cls) -> "Secrets":
        if cls._instance is None:
            cls._instance = super(Secrets, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Initialize the secrets from environment variables"""
        load_dotenv()
        self.MongoConnectionURL = os.getenv("MONGO_CONNECTION_URL", "")
        self.DBName = os.getenv("DB_NAME", "")
        self.TelegramAPIKey = os.getenv("TELEGRAM_API_KEY", "")
        self.BotToken = str(os.getenv("BOT_TOKEN"))
        self.GuildID = int(os.getenv("GUILD_ID"))


        if not self.MongoConnectionURL:
            raise ValueError("MONGO_CONNECTION_URL environment variable is not set")

        if not self.DBName:
            raise ValueError("DB_NAME environment variable is not set")

        if not self.TelegramAPIKey:
            raise ValueError("TELEGRAM_API_KEY environment variable is not set")
        
        if not self.BotToken:
            raise ValueError("BOT_TOKEN environment variable is not set")
        
        if not self.GuildID:
            raise ValueError("GUILD_ID environment variable is not set")
