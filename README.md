# Automating Python learning with Gemini

Learn new bits of Python with the help of Google Gemini! Leveraging the power of ever-evolving AI, this project
introduces users to automated, AI-powered learning.

## Table of Contents

- [Overview](#overview)
- [Goals](#goals)
- [Setup](#setup)
- [Usage](#usage)

## Overview

Google Gemini is an advanced LLM designed for generating and processing text. This project creates a unique learning
tool by utilizing the Google Gemini API in Python to send a prompt of the user's choice to a Gemini model of the user's
choice, and the subsequent response is emailed to a designated address. The Gemini Flash models are optimized for
generating quick, accurate text responses, making it ideal for automating learning tasks. The purpose of this app is to
have new Python tips and tricks automatically emailed to the user at an interval of their choice.

## Goals

My motivation for this project was to create a simple, AI-powered learning tool to help budding developers or anyone
just wanting to learn a couple new bits of Python. I hope other's find this program useful and are able to learn
something new from it, if that is the case, then I view this project as a success.

## Setup

1. If you have not already, you must set up SMTP/app usage for your email. It is highly recommended to use
   an app password instead of your actual password whenever possible.

   Please refer to the appropriate link below for your email provider:
    - [Outlook](https://mailtrap.io/blog/outlook-smtp/)
    - [Yahoo](https://mailtrap.io/blog/yahoo-smtp/)
    - [iCloud](https://mailtrap.io/blog/icloud-smtp/)
    - [Gmail](https://mailtrap.io/blog/gmail-smtp/)
    - [AOL](https://mailtrap.io/blog/aol-smtp/)
    - [ATT/Verizon](https://mailmeteor.com/smtp/att-smtp-settings)

2. Open your command line or terminal and clone the repository:
   ```bash
   git clone https://github.com/chrisF943/Gemini-Python-Tips.git
   ```
    - If you have GitHub Desktop select "Open with GitHub Desktop" from the green code dropdown.
3. If you do not already have one, get a Gemini API
   key [here](https://ai.google.dev/gemini-api/docs/api-key).
4. Create a .env file in the root directory of the project and fill in required credentials.
5. Open `config.py`, choose a provider you would like to use from the dictionaries and set `CHOSEN_PROVIDER`

   accordingly, for example: `CHOSEN_PROVIDER = "gmail"`.

6. Also in `config.py`, set `SAVE_LOGS` to `True` if you would like to save logs to a file, by default this is set to
   `False`.

## Usage

1. Navigate to the directory where you have cloned the project:
   ```bash
   cd path/to/project
   ```
   or on Windows:
   ```bash
   cd path\to\project
   ```
2. Create a virtual environment (You can skip to the next step if you already have one):
   ```bash
   python3 -m venv .venv
   ```
3. Activate your virtual environment:

   For macOS/Linux:
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

## Automation

*Note: For mac there are multiple options for automation, such as cron, launchd, and Automator. The example below uses
Automator and Calendar, as I believe it is the easiest to set up, and cron/launchd jobs can skip or delay execution if
your computer is off or asleep when the job is scheduled to run. If you wish to use cron or launchd, please refer to
the appropriate documentation here:*

- [How to create a cron job](https://phoenixnap.com/kb/cron-job-mac)
- [launchd tutorial](https://medium.com/@chetcorcos/a-simple-launchd-tutorial-9fecfcf2dbb3)
- [creating a timed launchd job](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html)

For Windows:

1. Open Task Scheduler
2. Create a new task
3. Set the trigger to run the task at the desired time
4. Set the start in to the project directory
5. Set the action to start a program and provide arguments to run the Python script:
   ```bash
   .\.venv\Scripts\activate && python3 main.py
   ```
6. Save the task

For macOS:

To reduce the chance of errors when running an automated job, it is recommended to allow full disk access for Terminal
and/or Automator if you are using it by going to the "Privacy & Security" section in System Preferences, then "Full Disk
Access" and add the relevant application(s)

1. Open Automator
2. Create a new document, then choose application
3. Add a "Run Shell Script" action and enter the commands to run the Python script, putting each on a new line:
   ```bash
   cd path/to/project
   source .venv/bin/activate
   python3 main.py
   ```
4. Save the job
5. Open Calendar and create a new event and give it a name
6. Set the time and interval you would like the event(Python script) to run at
7. Under "Alert" choose "Custom", then "Open File" and navigate to and select the job you created
8. Set the alert time to "At time of event"

*Developed on Python 3.12*
