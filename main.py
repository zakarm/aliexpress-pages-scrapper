from Bcolors import Bcolors as bc
from Product import Product
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

url = "https://best.aliexpress.com/?src=google&albch=fbrnd&acnt=304-410-9721&albcp=6451874585&albag=78594005233&slnk=&trgt=kwd-14803160428&plac=&crea=399444576449&netw=g&device=c&mtctp=b&memo1=&albbt=Google_7_fbrnd&albagn=888888&isSmbActive=false&isSmbAutoCall=false&needSmbHouyi=false&gad_source=1&gclid=CjwKCAiAiP2tBhBXEiwACslfnr86ff6arM3sRwUXWoCzSmQPMJQ1w-RU79BcEOSoHJfagY6rgIF50xoC6q4QAvD_BwE&aff_fcid=71543630b2784b89875677edf8ec424a-1707071211634-02765-UneMJZVf&aff_fsk=UneMJZVf&aff_platform=aaf&sk=UneMJZVf&aff_trace_key=71543630b2784b89875677edf8ec424a-1707071211634-02765-UneMJZVf&terminal_id=58f390e3ce4040458a6b8dfc5a059e5f&afSmartRedirect=y"
products = []

def export_data_to_csv():
    global products
    data = {"Title": [], "Rev_Rate": [], "Solde": [], "Shipping": [], "Price": []}
    for product in products:
        data["Title"].append(product.title)
        data["Rev_Rate"].append(product.rev_rate)
        data["Solde"].append(product.solde)
        data["Shipping"].append(product.shipping)
        data["Price"].append(product.price)
    df = pd.DataFrame(data)
    df.to_csv('aliexpress_products.csv', index=False)


def get_url_page():
    global url
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for i in range(1, 6):
        sleep(0.1)
        print(f"-> AliExpress Scrapper : {bc.WARNING}Waiting ...{bc.DEFAULT}")
    scroll_heigh = 88
    scroll_inc = 180 #change this increment arg to scrap more data !
    for _ in range(scroll_inc):
        driver.execute_script(f"window.scrollBy(0, {scroll_heigh});")
        sleep(0.4)
        print(f"-> AliExpress Scrapper : {bc.WARNING}Waiting ...{bc.DEFAULT}")
        try:
            more_to_love_button = WebDriverWait(driver, 0.1).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'more-to-love--action--2gSTocC'))
            )
            more_to_love_button.click()
            sleep(2)
            print(f"-> AliExpress Scrapper : {bc.WARNING}Waiting ...{bc.DEFAULT}")
        except Exception as e:
            pass
    html_content = driver.page_source
    driver.quit()
    return html_content


def scrap_products(soup_object):
    global products
    products_elements = soup_object.find_all("div", {"class": "recommend-card--card-wrap--2jjBf6S"})
    for p in products_elements:
        title_div = p.find('div', style="font-size: 14px; color: rgb(25, 25, 25); height: 18px; display: -webkit-box; overflow: hidden; text-overflow: ellipsis; -webkit-box-orient: vertical; -webkit-line-clamp: 1;")
        rev_rate_div = p.find('div', class_="rc-modules--stars--o9mzAea")
        solde_div = p.find('div', style="font-size: 12px; color: rgb(117, 117, 117);")
        shipping_div = p.find('span', class_="rc-modules--text--3kpyr_j")
        price_div = p.find('span', class_="rc-modules--price--1NNLjth")
        
        title_text = title_div.get('title') if title_div else ""
        rev_rate_text = rev_rate_div.get('title') if rev_rate_div else ""
        solde_text = solde_div.text if solde_div else ""
        shipping_text = shipping_div.text if shipping_div else ""
        price_text = price_div.text if price_div else ""

        product_object = Product(title_text, rev_rate_text, solde_text, shipping_text, price_text )
        product_object.description()
        products.append(product_object)


def main():
    print(f"-> AliExpress Scrapper : {bc.OKGREEN}Start{bc.DEFAULT}")
    html_page = get_url_page()
    soup_object = BeautifulSoup(html_page, 'html.parser')
    scrap_products(soup_object)
    export_data_to_csv()
    print(f"-> AliExpress Scrapper : {bc.FAIL}Down{bc.DEFAULT}")

if __name__ == "__main__":
    main()