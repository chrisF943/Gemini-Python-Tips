import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from src.prompt_handler import format_tips


def send_email(response):
    """
    Sends an HTML-formatted email containing the given response.

    This function constructs an email with the provided response as an HTML message body,
    with proper formatting for code blocks and text. It determines the SMTP provider from
    the configuration and sends the email using either SSL or TLS encryption based on
    the provider's settings.

    Parameters:
        response (str): The message content to be sent via email.

    Raises:
        Exception: Logs an error if the email fails to send.
    """
    try:
        logging.info("Sending email...")

        # HTML template with CSS styling
        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    margin-bottom: 30px;
                    text-align: center;
                }}
                .intro {{
                    font-size: 1.1em;
                    margin-bottom: 25px;
                    color: #555;
                    text-align: center;
                }}
                .tip {{
                    background-color: #f8f9fa;
                    border-left: 4px solid #007bff;
                    padding: 15px;
                    margin-bottom: 20px;
                }}
                .tip-title {{
                    display: block;
                    margin-bottom: 10px;
                    font-size: 1.1em;
                    color: #007bff;
                }}
                code {{
                    background-color: #f1f1f1;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    margin: 15px 0;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    display: block;
                    white-space: pre;
                }}
                strong {{
                    color: #007bff;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    text-align: center;
                    font-size: 0.9em;
                    color: #666;
                }}
                .footer a {{
                    color: #007bff;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>Your Daily Python Tips</h2>
                <div class="intro">Here are your daily Python tips and tricks, happy learning!</div>
            </div>
            {format_tips(response)}
            <div class="footer">
            <p>Generated with ❤️ by Gemini-Python-Tips, created by Christopher Faris</p>
        <p>Visit my <a href="https://github.com/chrisF943/">GitHub</a> or my <a href="https://chrisfaris.netlify.app/">Portfolio</a> to see more!</p>
            </div>
        </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "Your Daily Python Tips"
        msg["From"] = os.getenv("SENDER")
        msg["To"] = os.getenv("RECIPIENT")

        # Add both plain text and HTML versions
        msg.attach(MIMEText(response, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        chosen_provider = config.CHOSEN_PROVIDER.lower()
        if chosen_provider in config.SSL_PROVIDER_HOSTS:
            smtp_host = config.SSL_PROVIDER_HOSTS[chosen_provider]
            smtp_port = config.PROVIDER_PORTS["ssl"]
            logging.info(f"SSL was chosen for {chosen_provider}, using host: {smtp_host}.")
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
