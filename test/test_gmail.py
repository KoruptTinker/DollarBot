import pytest
from unittest.mock import patch, mock_open, MagicMock
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from code.gmail import GMailClient


@pytest.fixture
def gmail_client():
    return GMailClient(email="test@gmail.com", password="test_password")


class TestGMailClient:
    def test_init(self):
        client = GMailClient("test@gmail.com", "password")
        assert client._email_address == "test@gmail.com"
        assert client._password == "password"

    @patch("smtplib.SMTP")
    def test_send_email_without_attachment(self, mock_smtp):
        client = GMailClient("sender@gmail.com", "password")
        client.send_email(
            to_email="receiver@gmail.com",
            subject="Test Subject",
            content="Test Content",
        )

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_with("sender@gmail.com", "password")
        mock_smtp.return_value.sendmail.assert_called_once()
        mock_smtp.return_value.quit.assert_called_once()

    @patch("smtplib.SMTP")
    @patch("builtins.open", new_callable=mock_open, read_data=b"test data")
    def test_send_email_with_attachment(self, mock_file, mock_smtp):
        client = GMailClient("sender@gmail.com", "password")
        client.send_email(
            to_email="receiver@gmail.com",
            subject="Test Subject",
            content="Test Content",
            attachment="test.txt",
        )

        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        mock_file.assert_called_with("test.txt", "rb")
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_with("sender@gmail.com", "password")
        mock_smtp.return_value.sendmail.assert_called_once()
        mock_smtp.return_value.quit.assert_called_once()

    @patch("smtplib.SMTP")
    def test_email_headers(self, mock_smtp):
        client = GMailClient("sender@gmail.com", "password")
        with patch.object(
            MIMEMultipart, "as_string", return_value=""
        ) as mock_as_string:
            client.send_email(
                to_email="receiver@gmail.com",
                subject="Test Subject",
                content="Test Content",
            )

            call_args = mock_smtp.return_value.sendmail.call_args[0]
            assert call_args[0] == "sender@gmail.com"
            assert call_args[1] == "receiver@gmail.com"
