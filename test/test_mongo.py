import pytest
from unittest.mock import Mock, patch, MagicMock
from pymongo import MongoClient
from code.mongo import MongoDB


@pytest.fixture
def mock_models():
    with (
        patch("code.mongo.UsersModel") as users_mock,
        patch("code.mongo.SpendsModel") as spends_mock,
        patch("code.mongo.BudgetsModel") as budgets_mock,
        patch("code.mongo.LinkCodesModel") as link_codes_mock,
    ):
        yield {
            "users": users_mock,
            "spends": spends_mock,
            "budgets": budgets_mock,
            "link_codes": link_codes_mock,
        }


@pytest.fixture
def mongodb_instance(mock_models):
    with patch("pymongo.MongoClient") as mock_client:
        instance = MongoDB("mongodb://test", "test_db")
        instance._client = mock_client.return_value
        yield instance


class TestMongoDB:
    def test_singleton_pattern(self):
        db1 = MongoDB("mongodb://test1", "test_db1")
        db2 = MongoDB("mongodb://test2", "test_db2")
        assert db1 is db2
        assert db1._connection_url == "mongodb://test1"
        assert db1._db == "test_db1"

    @patch("certifi.where")
    @patch("pymongo.MongoClient")
    def test_connection(self, mock_client, mock_certifi):
        mock_certifi.return_value = "cert_path"
        MongoDB("mongodb://test", "test_db")
        assert not mock_client.called

    def test_cleanup(self, mongodb_instance):
        mongodb_instance.close()
        assert mongodb_instance._client is None

    def test_user_operations(self, mongodb_instance):
        # Test fetch_user_from_telegram

        # Test fetch_user_from_discord
        mongodb_instance.fetch_user_from_discord("456")

        # Test create_user_from_telegram
        assert mongodb_instance.create_user_from_telegram("123") == True
        assert mongodb_instance.create_user_from_telegram("") == False

    def test_spends_operations(self, mongodb_instance):
        # Test create_spends_from_telegram
        assert (
            mongodb_instance.create_spends_from_telegram(
                "123", "2024-01-01", "food", 100
            )
            == True
        )
        assert mongodb_instance.create_spends_from_telegram("", "", "", 0) == False

        # Test fetch_spends_from_telegram
        mongodb_instance.fetch_spends_from_telegram("123")

        # Test reset_spends_from_telegram
        assert mongodb_instance.reset_spends_from_telegram("123") == True
        assert mongodb_instance.reset_spends_from_telegram("") == False

    def test_budget_operations(self, mongodb_instance):
        # Test create_budget_from_telegram
        assert mongodb_instance.create_budget_from_telegram("123") == True
        assert mongodb_instance.create_budget_from_telegram("") == False

        # Test fetch_budget_from_telegram
        mongodb_instance.fetch_budget_from_telegram("123")

        # Test update_budget_from_telegram
        assert mongodb_instance.update_budget_from_telegram("123", "food", 500) == True
        assert mongodb_instance.update_budget_from_telegram("", "", 0) == False

    def test_link_code_operations(self, mongodb_instance):
        # Test create_link_code_from_telegram
        assert mongodb_instance.create_link_code_from_telegram(123, "CODE123") == True
        assert mongodb_instance.create_link_code_from_telegram(0, "") == False

        # Test create_link_code_from_discord
        assert mongodb_instance.create_link_code_from_discord(456, "CODE456") == True
        assert mongodb_instance.create_link_code_from_discord(0, "") == False

        # Test fetch_link_code
        mongodb_instance.fetch_link_code("CODE123")
