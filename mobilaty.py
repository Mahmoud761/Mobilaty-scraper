from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

product_name, new_price, old_price, links, brand = [], [], [], [], []
page_num = 0

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

while True:
    url = f"https://www.mobilaty.com/en/product/mobiles?page={page_num}"

    driver.get(url)

    # ✅  wait until the product instead 
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-title"))
        )
    except:
    
        print("❌ this page has no products or the site is down.")
        break
    # Take the page after downloading                
    soup = BeautifulSoup(driver.page_source, "lxml")
    # downloading item from page
    product_tags = soup.find_all("p", class_="product-title fade mb-0 pointer multiple-line-name ng-star-inserted")
    price_tags = soup.find_all("div", class_="defult-price-color payment-with-discount-container fs-xs-11 d-flex gap-10 mr-2 ng-star-inserted")
    old_price_tags = soup.find_all("div", class_="fs-12 fs-xs-10 bottom3 d-flex gap-10 defult-price-color-after-discount ng-star-inserted")
    
    if not product_tags:
        print("✅ No Items")
        break
    #  save data in variable list     
    for i in range(len(product_tags)):
        product_name.append(product_tags[i].get_text(strip=True))
        new_price.append(price_tags[i].get_text(strip=True) if i < len(price_tags) else "")
        old_price.append(old_price_tags[i].get_text(strip=True) if i < len(old_price_tags) else "")
        links.append("https://www.mobilaty.com" + product_tags[i].find("a").attrs["href"])

    print(f"✅ Page {page_num} scraped ({len(product_tags)} items)")
    page_num += 1

for link in links:
    driver.get(link)

    # ✅  wait until the product instead 
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-title"))
        )
    except:
    
        print("❌ this page has no products or the site is down.")
        brand.append("")
        continue

    # Take the page after downloading                
    soup = BeautifulSoup(driver.page_source, "lxml")
    brand_tag = soup.find("span",class_="brand-name")
    if brand_tag:
        brand.append(brand_tag.get_text(strip=True))
    else:
        brand.append("")
print("brand scraping done")       


driver.quit()

# save data
file_list = [product_name, new_price, old_price, links,brand]
exp = zip_longest(*file_list)

with open(r"D:\Study\web scraping\Mobilaty.csv", "w", newline='', encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["product name", "New Price", "Old Price","links","brand"])
    wr.writerows(exp)

print("✅ All data Saved ✅")











    






