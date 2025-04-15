import logging
import config
from dotenv import load_dotenv
from src.prompt_handler import send_prompt
from src.email_handler import send_email

load_dotenv()

# Configure logging
log_handlers: list = [logging.StreamHandler()]

# Add log saving to config if SAVE_LOGS is True
if config.SAVE_LOGS:
    log_handlers.append(logging.FileHandler("logs/app.log"))

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=log_handlers
)

if __name__ == "__main__":
    prompt_response = send_prompt()
    if prompt_response is not None:
        send_email(prompt_response)
