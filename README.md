# Coding Challenge
A Python-based solution for processing and analyzing a list of URLs.</br>
By Matt Dixon

## Description
This project provides a Python script that reads a list of URLs from a text file, processes each URL, and outputs a result of additonal hyperlinks on the page. It's designed to handle various URL processing tasks efficiently (and showcase knowledge to my potential employer :slightly_smiling_face:)

## Table of Contents
  * Installation
  * Usage
  * Features

## Installation
1. Clone the repository:

```
git clone https://github.com/MattDixon98/CodingChallenge.git
cd CodingChallenge
```
2. Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage
1. Prepare your list of URLs:
  * Add the URLs you wish to process to the url_list.txt file, with each URL on a new line.
2. Run the script:
```
python coding_challenge.py
```
3. View the output:</br>
  * Processed results will be saved in the output directory.

## Features
  * Reads URLs from a text file.
  * Processes each URL and extract the markup.
  * If there are many URLs, they will run concurrently
  * Creates a list of URLs found on the parent URL page
  * Several unit tests to validate different cases
  * Outputs results to a designated directory.
