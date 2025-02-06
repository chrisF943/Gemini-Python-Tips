# Automating Python learning with Gemini

Learn new bits of Python with the help of Google Gemini. This project is currently being worked on and developed.

## Overview

Google Gemini is an advanced LLM designed for generating and processing text. This project creates a unique learning
tool by utilizing the Google Gemini API in Python to send a prompt of the user's choice to the Gemini 1.5 Flash model
and the subsequent response is emailed to a designated address. The Gemini 1.5 Flash model is optimized for generating
quick, accurate text responses, making it ideal for automating learning tasks. The purpose of this app is to have new
Python tips and tricks automatically emailed to the user at an interval of their choice.

## Goals

My motivation for this project was to create a simple, AI-powered learning tool to help budding developers or anyone
just wanting to learn a couple new bits of Python. I hope other's find this program useful and are able to learn
something new from it, if that is the case, then I view this project as a success.

## Setup

1. Open your command line or terminal and clone the repository:
   ```bash
   git clone https://github.com/chrisF943/Gemini-Python-Tips.git
   ```
    - If you have GitHub Desktop select "Open with GitHub Desktop" from the green code dropdown.
2. If you do not already have one, get a Gemini API
   key [here](https://ai.google.dev/gemini-api/docs/api-key#macos---zsh).
3. Create a .env file in the root directory of the project and fill in required credentials.
4. Open `config.py`, choose a provider you would like to use from the dictionaries and set `CHOSEN_PROVIDER`

   accordingly, for example: `CHOSEN_PROVIDER = "gmail"`.

5. Also in `config.py`, set `SAVE_LOGS` to `True` if you would like to save logs to a file, by default this is set to
   `False`.

## Usage

1. Navigate to the directory where you have cloned the project:
   ```bash
   cd path/to/project
   ```
2. Create a virtual environment (You can skip to the next step if you already have one):
   ```bash
   python3 -m venv .venv
   ```
3. Activate your virtual environment:

   For MacOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

   For Windows:
   ```bash
   .\.venv\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
    - *Optional* Verify packages are installed:
      ```bash
      pip list
      ```
5. Run the program:
   ```bash
   python3 main.py
   ```
6. When done, deactivate your virtual environment:
   ```bash
   deactivate
   ```

## Contributing
