import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
import google.generativeai as genai
import datetime
import logging
import config
from dotenv import load_dotenv

# TODO: repackage code into modules

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


# Get current day as integer (for setting run interval based on day of week, if needed)
# today = datetime.date.today()
# day = today.weekday()


def send_prompt():
    """
    Generates a prompt requesting three unique Python tips and tricks.

    This function initializes the Generative AI model, sends a prompt
    requesting three unique Python tips, and returns the generated response.

    Returns:
        str: The generated response containing three Python tips.
        None: If an error occurs.
    """
    try:
        logging.info("Sending prompt...")
        genai.configure(api_key=os.getenv("API_KEY"))

        model = genai.GenerativeModel(config.CHOSEN_MODEL)
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

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error("send_prompt() failed.")


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
        <p>Visit our <a href="https://github.com/chrisF943/Gemini-Python-Tips">GitHub repository</a> for more information</p>
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


def format_tips(response):
    """
    Formats the response text into HTML with proper styling for code blocks.
    
    Parameters:
        response (str): The raw response from the AI
        
    Returns:
        str: HTML formatted content
    """
    # Split the text into tips using numbered points as delimiters
    tips = re.split(r'\n*\d+\.\s+', response)
    # Remove any empty strings from the split and skip the initial response sentence
    tips = [tip for tip in tips if tip.strip()]
    if tips and "Python tips" in tips[0]:  # Check if first item is the intro sentence
        tips = tips[1:]  # Skip the model's intro

    formatted_tips = []
    for tip in tips:
        if tip.strip():
            formatted_tip = tip

            # Handle title formatting (text between ** and :)
            title_pattern = r'\*\*(.*?):\*\*'
            formatted_tip = re.sub(
                title_pattern,
                lambda m: f'<strong class="tip-title">{m.group(1)}:</strong><br>',
                formatted_tip
            )

            # Find all code blocks (text between triple backticks with optional language specification)
            code_block_pattern = r'```(?:python)?\n(.*?)```'
            formatted_tip = re.sub(
                code_block_pattern,
                lambda m: f'<pre><code>{m.group(1).strip()}</code></pre>',
                formatted_tip,
                flags=re.DOTALL
            )

            # Handle inline code (text between single backticks)
            inline_code_pattern = r'`([^`]+)`'
            formatted_tip = re.sub(
                inline_code_pattern,
                lambda m: f'<code>{m.group(1)}</code>',
                formatted_tip
            )

            # Wrap each tip in a div with a number
            tip_number = len(formatted_tips) + 1
            formatted_tips.append(
                f'<div class="tip">'
                f'<strong>{tip_number}.</strong> {formatted_tip}'
                f'</div>'
            )

    return '\n'.join(formatted_tips)


if __name__ == "__main__":
    prompt_response = send_prompt()
    if prompt_response is not None:
        send_email(prompt_response)
