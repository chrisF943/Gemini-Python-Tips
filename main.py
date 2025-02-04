import smtplib
from email.mime.text import MIMEText
import os
import google.generativeai as genai
import datetime
import logging
import config
from dotenv import load_dotenv

load_dotenv()

# Configure logging
log_handlers = [logging.StreamHandler()]

if config.SAVE_LOGS:
    log_handlers.append(logging.FileHandler("logs/app.log"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=log_handlers
)

today = datetime.date.today()
day = today.weekday()


def send_prompt():
    if day == 1:
        logging.info("Sending prompt...")
        genai.configure(api_key=os.getenv("API_KEY"))

        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = model.generate_content(
            """
            Give me 3 small, intermediate to advanced Python tips and tricks to make
            my projects better and more efficient. Please give me exactly 3 unique, different
            tips everytime you are asked this prompt.
    
            """
        )
        generated_response = prompt.text
        logging.info("send_prompt() executed successfully.")
        return generated_response
    else:
        logging.info("Skipped execution today.")
        return None


def send_email(response):
    logging.info("Sending email...")
    msg = MIMEText(response, "plain", "utf-8")
    msg["Subject"] = "Your Daily Python Tips"
    msg["From"] = os.getenv("SENDER")
    msg["To"] = os.getenv("RECIPIENT")

    try:
        chosen_provider = config.CHOSEN_PROVIDER.lower()
        if chosen_provider in config.SSL_PROVIDER_HOSTS:
            smtp_host = config.SSL_PROVIDER_HOSTS[chosen_provider]
            smtp_port = config.PROVIDER_PORTS["ssl"]
            logging.info(f"SSl was chosen for {chosen_provider}, using host: {smtp_host}.")
            logging.info(f"Running on port {smtp_port}.")
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as connection:
                connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
                connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

            logging.info("send_email() executed successfully.")

        elif chosen_provider in config.TLS_PROVIDER_HOSTS:
            smtp_host = config.TLS_PROVIDER_HOSTS[chosen_provider]
            smtp_port = config.PROVIDER_PORTS["tls"]
            logging.info(f"TLS was chosen for {chosen_provider}, using host: {smtp_host}.")
            logging.info(f"Running on port {smtp_port}.")
            with smtplib.SMTP(smtp_host, smtp_port) as connection:
                connection.starttls()
                connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
                connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

            logging.info("send_email() executed successfully.")

        else:
            logging.warning("Chosen provider not recognized, see configuration file for supported providers.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error("send_email() failed.")


if __name__ == "__main__":
    prompt_response = send_prompt()
    if prompt_response is not None:
        send_email(prompt_response)
