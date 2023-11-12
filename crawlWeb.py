# Prepare
#   1. Install chrome browser
#   2. Install python3
#   3. Install PIP and requirement library by run install.bat

# Usage:
#   1. Input list of url to a text file, for example "ex1_links_non_scrollable.txt"
#   2. Run command as below to crawl data
#           python crawlweb.py <url list file>
#
#      For example: 
#           python crawlweb.py ex1_links_non_scrollable.txt

# Documents reference:
# https://beautiful-soup-4.readthedocs.io/en/latest/
# https://selenium-python.readthedocs.io/installation.html

#Example url for extract data webpage
# https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
# https://support.atlassian.com/jira-software-cloud/docs/jql-functions/

# https://www.nike.com/gb/w/mens-shoes-nik1zy7ok

import sys
import os
import glob
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

SCROLL_SLEEP=5 #second


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

#DO NOT USE
def example():
    soup = BeautifulSoup(html_doc, 'html.parser')

    print(soup.p["class"]) # ['title']

    #get attribute of tag
    print(soup.a["href"]) # http://example.com/elsie
    print(soup.a["class"]) # ['sister']
    print(soup.a["id"]) # link1
    print(soup.a.text) # Elsie

    #find tag with attribute
    print("\n\n")
    links = soup.find_all("a", class_="sister", id="link1")
    for link in links:
        print(link.text) #Elsie

    links = soup.find_all("a", class_="sister", href="http://example.com/tillie")
    for link in links:
        print(link.text) #Tillie


    print("\n\n")
    links = soup.find_all("a")
    for link in links:
        print(link.get('href'))

    print("\n\n")
    links = soup.find_all(id="link1")
    for link in links:
        print(link.text)

    print("\n\n")
    links = soup.find_all(class_="sister")
    for link in links:
        print(link.text)

#DO NOT USE
def scan_files():
    folder_path = os.getcwd()

    # # Get a list of all files in the folder
    # file_list = os.listdir(folder_path)

    # # Iterate over the file list
    # for file_name in file_list:
    #     file_path = os.path.join(folder_path, file_name)
    #     if os.path.isfile(file_path):
    #         # Process the file
    #         print(file_name)

    html_files = glob.glob(os.path.join(folder_path, "*.html"))
    # Iterate over the HTML files
    for file_path in html_files:
        # Process the HTML file
        print("Found:", file_path)

def get_url_list(url_input_file):
    url_list = open(url_input_file, 'r')
    return url_list.readlines()

def load_webpage_by_request(url):
    url = url.strip()
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Open link error: {response.status_code}")
        return None
    return response.content

def load_webpage_by_browser(url):
    #Scroll down load more
    driver = webdriver.Chrome() 
    driver.get(url)

    # Get initial scroll height
    # last_height = driver.execute_script("return document.body.scrollHeight")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    # print(f"last_height: {last_height}")
    scroll_down_counter = 0
    while True:
        # Scroll down to the bottom of the page
        element_body = driver.find_elements(By.TAG_NAME, "body")
        for element in element_body:
            element.send_keys(Keys.END)

        # Wait for a short interval to allow the page to load
        time.sleep(SCROLL_SLEEP)
        
        # Calculate new scroll height and compare with the last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop if the scroll height hasn't changed

        scroll_down_counter = scroll_down_counter + 1
        print(f"Next scroll down: {scroll_down_counter}") 
        last_height = new_height

    # #scroll down
    # for i in range(1,20):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(10)

    full_html = driver.page_source
    driver.quit()
    return full_html

def save_file(save_content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        # Write the text to the file
        # file.write(soup.text)
        file.writelines(save_content)


def extract_webpage_data_ex1(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all("div", class_="pm-table-wrapper")
    for table_id, table in enumerate(tables):
        print(f"\n\nTable: {table_id + 1}")
        rows = table.find_all("tr")
        for row_id, row in enumerate(rows):
            col1 = row.find("p")
            col2 = row.find("td")
            col2Text = col2.text
            col2Text = col2Text.replace("\n", " ")
            print(f"row: {row_id} / {col1.text} - {col2Text}")

def extract_webpage_data_ex2(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    products = soup.find_all(class_="product-card__info")
    for product_id, product in enumerate(products):
        print(f"Product: {product_id} - {product.text}")

def main():
    arguments  = sys.argv
    if (len(arguments) != 2) or (arguments [1] is None) or (len(arguments [1]) == 0):
        print("Please input url list file")
        return
    
    print(f"Url list file: {arguments [1]} ")

    urls = get_url_list(arguments [1])
    number_of_url = len(urls)
    print(f"Number of url: {number_of_url} \n\n")
    for url_id, url in enumerate(urls):
        url_strip = url.strip()
        print(f"{url_id + 1}  - {url_strip}")
        html_content = load_webpage_by_browser(url_strip)
        if (html_content is None) or (not html_content):
            print(f"Load webpage failed !")
            continue
    
        extract_webpage_data_ex1(html_content)
        print("\n\n")

if __name__ == '__main__':
    print("\n\n----- MAIN Start------")
    main()
    print("----- MAIN End------")