# AliExpress Scrapper

## Overview

This script is a web scraper designed to extract product information from AliExpress, a popular online shopping platform. It utilizes the Selenium and BeautifulSoup libraries to navigate and parse the HTML content of the AliExpress website, and then exports the gathered data into a CSV file.

## Prerequisites

Make sure you have the following dependencies installed:

- Python 3.x
- Selenium
- BeautifulSoup
- Pandas
- Chrome browser installed (with compatible version of ChromeDriver)

Install the required Python libraries using:

```bash
pip3 install -r requirements.txt
```

### Usage

1. Set up your environment by installing the required libraries.
2. Adjust the ChromeDriver path in the script based on your system configuration.

Run the script:
```bash
python aliexpress_scrapper.py
```

3. The script will open a Chrome browser, navigate to the specified AliExpress URL, scroll through the page to load more products, and then extract information such as title, review rate, sold quantity, shipping details, and price for each product.
4. The gathered data will be exported to a CSV file named aliexpress_products.csv.


### Customization
- You can customize the script by modifying the scroll_inc variable in the get_url_page function to control the number of times the page is scrolled for more data.
- Adjust the Chrome browser options in the get_url_page function if needed.

### Disclaimer
This script is for educational purposes only. Use it responsibly and adhere to AliExpress's terms of service.
