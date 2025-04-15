import os
import datetime
import logging
import google.generativeai as genai
import re
import config


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

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        model = genai.GenerativeModel(config.CHOSEN_MODEL)
        prompt = model.generate_content(
            f"""
            Give me 3 small, intermediate to advanced Python tips and tricks for improved 
            and more efficient code. The tips should contain concepts and functions that have not been 
            in a previous response (unique to this response). For each tip provide a brief example code snippet. 
            Please do not use any markdown formatting in your response except for code blocks. 
            Current time: {current_time}
            """,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                candidate_count=1,
                top_p=0.8,
                top_k=40,
                stop_sequences=None,
            )
        )
        generated_response = prompt.text
        logging.info("send_prompt() executed successfully.")
        return generated_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error("send_prompt() failed.")


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

            # Handle title formatting (looking for "Title: Description" pattern)
            title_pattern = r'^([^:]+):\s*(.*)$'
            match = re.match(title_pattern, formatted_tip, re.DOTALL)
            if match:
                title, content = match.groups()
                formatted_tip = f'<strong class="tip-title">{title.strip()}:</strong><br>{content.strip()}'

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
