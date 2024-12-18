# Matt Dixon 18.12.24

import re
import os
import sys
import shutil
import subprocess

# Function to install libraries from a requirements.txt file
def install_requirements():
    try:
        with open('requirements.txt', 'r') as f:
            packages = f.read().splitlines()
            for package in packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except FileNotFoundError:
        print("requirements.txt file not found. Ensure it exists in the same directory.")
        sys.exit(1)

# Call the function to install libraries
install_requirements()

import requests
from queue import Queue 
from threading import Thread
from bs4 import BeautifulSoup

# Global Queue variable
queue = Queue()

# Clean a list of URLs so just real URLs are returned
def clean_urls(urls):
    # Remove duplicates from the list
    urls = list(dict.fromkeys(urls))

    # Remove any items that don't start with 'https://' or 'http://'
    urls = [url for url in urls if url.startswith(("https://", "http://"))]

    return urls

def producer(links):
    # For each link, extract the markup
    for link in links:
        # Error handling in case an invalid URL is passed
        try:
            page = requests.get(link)
        except:
            continue

        # Split the string to find the name of the URL
        #   Need to split by both '//' and '.' in case the website doesn't contain 'www'
        split_link = re.split(r'[//.]+', link)
        name = split_link[1]
        if name == 'www':
            name = split_link[2]

        # Store the data in a dictionary
        queue_item = {
            'name': name, # Name for the output file
            'html': BeautifulSoup(page.text, 'html.parser')  # Extracted markup
        }

        queue.put(queue_item)

    # Add a sentinel value to indicate the producer is done
    queue.put(None)

def consumer():
    while True:
        item = queue.get()

        # Check for the sentinel value to terminate the consumer
        if item is None:
            break

        # Define an empty list to hold URLs from a page
        urls = []

        # Find all elements that have the 'a' tag with a 'href'
        for a in item['html'].find_all('a', href=True):
            # Pull just the 'href' information
            urls.append(a['href'])

        # Find all elements that have the 'link' tag with a 'href'
        for link in item['html'].find_all('link', href=True):
            # Pull just the 'href' information
            urls.append(link['href'])

        # Remove any duplicates from the list
        urls = clean_urls(urls)

        # Save the list to a file
        with open(f"output/{item['name']}.txt", 'w') as f:
            for line in urls:
                f.write(f"{line}\n")

def main(links):
    # Drop and re-create the 'output' folder to hold the data
    pth = os.path.join(os.getcwd(), 'output')
    shutil.rmtree(pth)
    os.mkdir(pth)

    t1 = Thread(target=consumer, args=())
    t2 = Thread(target=producer, args=(links,))

    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()

    print("Processing complete.")


if __name__ == '__main__':
    # Pass the text file and extract each line of text
    with open("url_list.txt", "r") as myfile:
        links = myfile.read().splitlines()
    
    main(links)