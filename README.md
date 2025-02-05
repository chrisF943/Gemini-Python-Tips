# Automating Python learning with Gemini

Learn new bits of Python with the help of Google Gemini. This project is currently being worked on and developed.

## Overview

Google Gemini is an advanced LLM designed for generating and processing text. This project creates a unique learning
tool by utilizing the Google Gemini API in Python to send a prompt of the user's choice to the Gemini 1.5 Flash model
and the subsequent response is emailed to a designated address. The Gemini 1.5 Flash model is optimized for generating
quick, accurate text responses, making it ideal for automating learning tasks. The purpose of this app is to have new
Python tips and tricks automatically emailed to the user at an interval of their choice.

## Goals

My goal for this project is to enhance my familiarity using LLM's with Python, doing so with practical use cases.

## Setup

1. Open your command line or terminal and clone the repository:
   `git clone https://github.com/chrisF943/Gemini-Python-Tips.git`, or if you have GitHub Desktop select "Open with
   GitHub Desktop" from the green code dropdown.
2. If you do not already have one, get a Gemini API
   key [here](https://ai.google.dev/gemini-api/docs/api-key#macos---zsh).
3. Create a .env file in the root directory of the project and fill in required credentials.
4. Open `config.py`, choose a provider you would like to use from the dictionaries and set `CHOSEN_PROVIDER`

   accordingly, for example: `CHOSEN_PROVIDER = "gmail"`.

5. Also in `config.py`, set `SAVE_LOGS` to `True` if you would like to save logs to a file, by default this is set to
   `False`.

## Usage

1. Navigate to the directory where you have cloned the project: `cd path/to/project`.
2. run `python3 -m venv .venv`
3. On Windows, run `.\.venv\Scripts\activate` or on Mac/Linux, run `source .venv/bin/activate`.
    1. If you already have a virtual environment (Some IDE's may create one for you when opening the project), run

       `source .venv/bin/activate` on Mac/Linux or `.\.venv\Scripts\activate` on Windows.
4. Run `pip install -r requirements.txt` to install the required packages.
    1. *Optional* run `pip list` to verify packages are installed.
5. Run `python3 main.py`,
6. When done, run `deactivate` to deactivate the virtual environment.

## Contributing
