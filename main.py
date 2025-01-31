import smtplib
from email.mime.text import MIMEText
import os
import google.generativeai as genai
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

today = datetime.date.today()
day = today.weekday()

ssl_providers = ["Gmail", "AOL", "ATT", "Verizon", "Comcast"]
tls_providers = ["Outlook", "Yahoo"]

chosen_provider = "gmail"


def send_prompt():
    if day == 0 or day == 2 or day == 4:
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
        if chosen_provider.lower() in [provider.lower() for provider in ssl_providers]:
            logging.info("SSl was chosen.")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
                connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

        elif chosen_provider.lower() in [provider.lower() for provider in tls_providers]:
            logging.info("TLS was chosen.")
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
                connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

        else:
            logging.warning("Chosen provider not recognized, please choose a provider from one of the lists.")

        logging.info("Email sent successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    prompt_response = send_prompt()
    if prompt_response is not None:
        send_email(prompt_response)
