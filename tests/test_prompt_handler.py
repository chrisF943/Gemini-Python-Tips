import pytest
from unittest.mock import patch, MagicMock
import os
import datetime
import google.generativeai as genai
import re
from src.prompt_handler import send_prompt, format_tips


class TestSendPrompt:
    @patch('src.prompt_handler.genai.configure')
    @patch('src.prompt_handler.genai.GenerativeModel')
    @patch('src.prompt_handler.os.getenv')
    @patch('src.prompt_handler.datetime.datetime')
    def test_send_prompt_success(self, mock_datetime, mock_getenv, mock_model_class, mock_configure):
        # Setup mocks
        mock_getenv.return_value = "fake_api_key"
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01 12:00:00"

        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Generated response text"
        mock_model.generate_content.return_value = mock_response

        # Call function
        result = send_prompt()

        # Assertions
        mock_configure.assert_called_once_with(api_key="fake_api_key")
        mock_model_class.assert_called_once()
        mock_model.generate_content.assert_called_once()
        assert result == "Generated response text"

    @patch('src.prompt_handler.genai.configure')
    @patch('src.prompt_handler.logging')
    def test_send_prompt_exception(self, mock_logging, mock_configure):
        # Setup mock to raise exception
        mock_configure.side_effect = Exception("API Error")

        # Call function
        result = send_prompt()

        # Assertions
        assert result is None
        mock_logging.error.assert_any_call("An error occurred: API Error")
        mock_logging.error.assert_any_call("send_prompt() failed.")


class TestFormatTips:
    def test_format_tips_with_empty_response(self):
        result = format_tips("")
        assert result == ""

    def test_format_tips_with_intro_sentence(self):
        response = "Here are some Python tips for you:\n1. First tip"
        result = format_tips(response)
        assert "First tip" in result
        assert "Python tips" not in result

    def test_format_tips_with_title_pattern(self):
        response = "1. Using Context Managers: They help manage resources efficiently"
        result = format_tips(response)
        assert '<strong class="tip-title">Using Context Managers:</strong>' in result

    def test_format_tips_with_code_blocks(self):
        response = "1. List Comprehensions:\n```python\nnumbers = [x for x in range(10)]\n```"
        result = format_tips(response)
        assert '<pre><code>numbers = [x for x in range(10)]</code></pre>' in result

    def test_format_tips_with_inline_code(self):
        response = "1. Use `enumerate()` instead of tracking indices manually"
        result = format_tips(response)
        assert '<code>enumerate()</code>' in result

    def test_format_tips_with_multiple_tips(self):
        response = "1. First tip\n2. Second tip\n3. Third tip"
        result = format_tips(response)
        assert '<strong>1.</strong>' in result
        assert '<strong>2.</strong>' in result
        assert '<strong>3.</strong>' in result
