import pytest
from unittest.mock import patch, MagicMock, call
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from src.email_handler import send_email


class TestSendEmail:
    @pytest.fixture
    def mock_env_vars(self):
        with patch.dict(os.environ, {
            "SENDER": "test@example.com",
            "RECIPIENT": "recipient@example.com",
            "PASSWORD": "test_password"
        }):
            yield

    @pytest.fixture
    def sample_response(self):
        return "1. Use f-strings for formatting\n```python\nname = 'World'\nprint(f'Hello, {name}!')\n```"

    @patch('src.email_handler.format_tips')
    @patch('src.email_handler.smtplib.SMTP_SSL')
    @patch('src.email_handler.config.CHOSEN_PROVIDER', 'gmail')
    @patch('src.email_handler.config.SSL_PROVIDER_HOSTS', {'gmail': 'smtp.gmail.com'})
    @patch('src.email_handler.config.PROVIDER_PORTS', {'ssl': 465})
    def test_send_email_ssl_provider(self, mock_smtp_ssl, mock_format_tips, mock_env_vars, sample_response):
        # Setup mocks
        mock_format_tips.return_value = "<div>Formatted HTML</div>"
        mock_connection = MagicMock()
        mock_smtp_ssl.return_value.__enter__.return_value = mock_connection

        # Call function
        send_email(sample_response)

        # Assertions
        mock_smtp_ssl.assert_called_once_with('smtp.gmail.com', 465)
        mock_connection.login.assert_called_once_with("test@example.com", "test_password")
        mock_connection.sendmail.assert_called_once()
        # Verify the first arg of sendmail is the sender
        assert mock_connection.sendmail.call_args[0][0] == "test@example.com"
        # Verify the second arg of sendmail is the recipient
        assert mock_connection.sendmail.call_args[0][1] == "recipient@example.com"

    @patch('src.email_handler.format_tips')
    @patch('src.email_handler.smtplib.SMTP')
    @patch('src.email_handler.config.CHOSEN_PROVIDER', 'outlook')
    @patch('src.email_handler.config.TLS_PROVIDER_HOSTS', {'outlook': 'smtp-mail.outlook.com'})
    @patch('src.email_handler.config.PROVIDER_PORTS', {'tls': 587})
    def test_send_email_tls_provider(self, mock_smtp, mock_format_tips, mock_env_vars, sample_response):
        # Setup mocks
        mock_format_tips.return_value = "<div>Formatted HTML</div>"
        mock_connection = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_connection

        # Call function
        send_email(sample_response)

        # Assertions
        mock_smtp.assert_called_once_with('smtp-mail.outlook.com', 587)
        mock_connection.starttls.assert_called_once()
        mock_connection.login.assert_called_once_with("test@example.com", "test_password")
        mock_connection.sendmail.assert_called_once()

    @patch('src.email_handler.logging')
    @patch('src.email_handler.config.CHOSEN_PROVIDER', 'invalid_provider')
    def test_send_email_invalid_provider(self, mock_logging, mock_env_vars, sample_response):
        # Call function
        send_email(sample_response)

        # Assertions
        mock_logging.warning.assert_called_once_with(
            "Chosen provider not recognized, see configuration file for supported providers."
        )

    @patch('src.email_handler.smtplib.SMTP_SSL')
    @patch('src.email_handler.config.CHOSEN_PROVIDER', 'gmail')
    @patch('src.email_handler.config.SSL_PROVIDER_HOSTS', {'gmail': 'smtp.gmail.com'})
    @patch('src.email_handler.config.PROVIDER_PORTS', {'ssl': 465})
    @patch('src.email_handler.logging')
    def test_send_email_exception(self, mock_logging, mock_smtp_ssl, mock_env_vars, sample_response):
        # Setup mock to raise exception
        mock_smtp_ssl.side_effect = Exception("SMTP Error")

        # Call function
        send_email(sample_response)

        # Assertions
        mock_logging.error.assert_any_call("An error occurred: SMTP Error")
        mock_logging.error.assert_any_call("send_email() failed.")
