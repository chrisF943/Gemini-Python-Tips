import smtplib
from email.mime.text import MIMEText
import os
import google.generativeai as genai
import datetime

today = datetime.date.today()
day = today.weekday()

ssl_providers = ["Gmail", "AOL", "ATT", "Verizon", "Comcast"]
tls_providers = ["Outlook", "Yahoo"]

chosen_provider = "gmail"

if day == 0 or day == 2 or day == 4:
    genai.configure(api_key=os.getenv("API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        """
        Give me 3 small, intermediate to advanced Python tips and tricks to make
        my projects better and more efficient. Please give me exactly 3 unique, different
        tips everytime you are asked this prompt.

        """
    )

    print(response.text)

    subject = "Your Daily Python Tips"
    msg = MIMEText(response.text, "plain", "utf-8")
    msg["Subject"] = "Your Daily Python Tips"
    msg["From"] = os.getenv("SENDER")
    msg["To"] = os.getenv("RECIPIENT")

    if chosen_provider.lower() in [provider.lower() for provider in ssl_providers]:
        print("you chose ssl")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
            connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

    elif chosen_provider.lower() in [provider.lower() for provider in tls_providers]:
        print("you chose tls")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(os.getenv("SENDER"), os.getenv("PASSWORD"))
            connection.sendmail(os.getenv("SENDER"), os.getenv("RECIPIENT"), msg.as_string())

    else:
        print("Provider not recognized, please enter a provider from one of the lists.")

else:
    print("No tips today.")

if __name__ == "__main__":
    pass
