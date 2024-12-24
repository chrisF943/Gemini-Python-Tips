# Automating Python learning with Gemini
Learn new bits of Python with the help of Google Gemini. **\*\*Work in progress\*\***.

## Overview
Google Gemini is an advanced LLM designed for generating and processing text. This project creates a unique learning tool by utilizing the Google Gemini API in Python to send a prompt of the user's choice to the Gemini 1.5 Flash model and the subsequent response is emailed to a designated address. The Gemini 1.5 Flash model is optimized for generating quick, accurate text responses, making it ideal for automating learning tasks. The purpose of this script is to have new Python tips and tricks automatically emailed somewhere on an interval.

## Goals
My goal for this project is to enhance my familiarity using LLM's with Python, doing so with practical use cases. Next updates will include training and tuning the model to further fine tune output.

## Usage
The prompt can be reconfigured to suit whatever your needs may be, in the case of this project it is to gather Python information. When running this script make sure all environment variables are properly set and all necessary packages are installed. Feel free to use the contents of this project for your own personal use and modification. Edits/pull requests are welcome!

## Requirements
All packages used simply need to be imported, except for the Gemini API library which can be installed via `pip install google-generativeai`. The version used in this project is `0.8.3`. A Google Gemini API key can be acquired for free [here](https://aistudio.google.com/app/apikey).

## Notes
When using the Gemini API a warning message will be displayed in the console from the underlying libraries, to avoid this you may set the versions of the `grpcio` and `grpcio-status` packages to 1.67.1 or similar with `pip install grpcio=={version} grpcio-status=={version}`. Depending on your account type be mindful of token and request limits when interacting with a LLM API. With a standard free Google account the 1.5 Flash model, used in this project, is limited to 15 requests per minute/1,000,000 tokens per minute. 

***This project was developed on Python version 3.12.***