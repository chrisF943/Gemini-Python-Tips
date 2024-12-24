# Learning Python With Gemini
Interacting with and training Google Gemini via Python. **\*\*Work in progress\*\***.

## Overview
This project utilizes the Google Gemini API in Python to send a prompt of the user's choice to the Gemini 1.5 Flash model and the subsequent response is emailed to a designated address. The purpose of this script is to have new Python tips and tricks automatically emailed somewhere on an interval.

## Goals
My personal goal for this project is to gain more experience working with LLM's, like Gemini while also broadening my knowledge and skills of Python. This is why the prompt is configured to it's current state. Next updates will include training and tuning the model.

## Usage
The prompt can be reconfigured to suit whatever your needs may be, in the case of this project the purpose is to gather Python information. When running this script make sure all environment variables are properly set and all necessary packages are installed. Feel free to use the contents of this project for your own personal use and modification. Edits/pull requests are welcome!

## Requirements
All packages used simply need to be imported, except for the Gemini API library which can be installed via `pip install google-generativeai`. The version used in this project is `0.8.3`

## Notes
When using the Gemini API a warning message will be displayed in the console from the underlying libraries, to avoid this you may set the versions of the `grpcio` and `grpcio-status` packages to 1.67.1 or similar with `pip install grpcio=={version} grpcio-status=={version}`. Depending on your account type be mindful of token and request limits when interacting with a LLM API. With a standard free Google account the 1.5 Flash model, used in this project, is limited to 15 requests per minute/1,000,000 tokens per minute.