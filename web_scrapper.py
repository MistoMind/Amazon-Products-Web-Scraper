import requests
from bs4 import BeautifulSoup
import pandas as pd

names = []
prices = []
ratings = []
no_reviews = []
urls = []
description = []
asin = []
manufacturer = []

for i in range(0, 15):
    URL = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}"

    header = {
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }
    response = requests.get(url=URL, headers=header).text

    soup = BeautifulSoup(response, "lxml")
    soup = soup.find(name='div', class_='s-main-slot s-result-list s-search-results sg-row')

    for product in soup.contents:
        if product.name == 'div':
            if int(product['data-index']) >=2 and int(product['data-index']) <= 25:
                # print(product['data-index'])
                details = product.find(name='div', class_='sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right')
                # print(details)
                if details != None:
                    url = "https://www.amazon.in" + details.find(name='a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')['href']
                    name = details.find(name='span', class_='a-size-medium a-color-base a-text-normal').string
                    price = details.find(name='div', class_='a-row a-size-base a-color-base')
                    # Check if product is Temporarily out of stock.
                    if price != None:
                        price = price.find(name='span', class_='a-offscreen').string
                        rating = details.find(name='span', class_='a-icon-alt').string
                        reviews = details.find(name='span', class_='a-size-base s-underline-text').string
                        names.append(name)
                        prices.append(price)
                        ratings.append(rating)
                        no_reviews.append(reviews)
                        urls.append(url)

                        response = requests.get(url=url, headers=header).text
                        print(url)

                        soup = BeautifulSoup(response, "lxml")

                        find_desc = soup.find('div', {'id': 'feature-bullets'})
                        temp = ""
                        for desc in find_desc.find_all('span', class_='a-list-item'):
                            temp = temp + desc.string + "\n"
                        description.append(temp)

                        # Checking if Product Details is in tabular form or list form
                        if soup.find('table', {'id': 'productDetails_detailBullets_sections1'}) != None:
                            # For Tabular Formatted Product Details
                            find_manufacturer = soup.find('table', {'id': 'productDetails_techSpec_section_1'})
                            all_types = find_manufacturer.find_all(name='th', class_='a-color-secondary a-size-base prodDetSectionEntry')
                            all_values = find_manufacturer.find_all(name='td', class_='a-size-base prodDetAttrValue')
                            for i in range(0, len(all_types)):
                                if all_types[i].string.strip() == 'Manufacturer':
                                    manufacturer.append(all_values[i].string.strip())
                                    break

                            find_asin = soup.find('table', {'id': 'productDetails_detailBullets_sections1'})
                            asin.append(find_asin.find(name='td', class_='a-size-base prodDetAttrValue').string)
                        else:
                            # For List Formatted Product Details
                            soup = soup.find(name='ul', class_='a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list')
                            for item in soup.find_all(name='span', class_='a-list-item'):
                                type = item.contents[1].string.split(' ')[0]
                                if type == 'Manufacturer\n':
                                    manufacturer.append(item.contents[3].string)
                                if type == 'ASIN\n':
                                    asin.append(item.contents[3].string)

data = pd.DataFrame({
    'Name': names, 
    'Price': prices, 
    'Rating': ratings, 
    'Number of Reviews': no_reviews, 
    'URL': urls,
    'Description': description,
    'ASIN': asin,
    'Manufacturer': manufacturer
})

print(data)
data.to_csv("Amazon Product List part 2.csv")
