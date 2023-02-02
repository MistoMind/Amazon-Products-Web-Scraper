import requests
from bs4 import BeautifulSoup

description = []
asin = []
manufacturer = []

# TABULAR_URL = "https://www.amazon.in/HEROZ-Backpack-Resistant-Durable-Notebook/dp/B08BYQZYYC/ref=sr_1_12_sspa?crid=2M096C61O4MLT&keywords=bags&qid=1675253937&sprefix=ba%2Caps%2C283&sr=8-12-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9tdGY&th=1"
TABULAR_URL = "https://www.amazon.in/American-Tourister-AMT-SCH-02/dp/B07CJCGM1M/ref=sr_1_3?crid=2M096C61O4MLT&keywords=bags&qid=1675342319&sprefix=ba%2Caps%2C283&sr=8-3"
LIST_URL = "https://www.amazon.in/Safari-Backpack-Resistant-Polyester-Travelling/dp/B09B26VHXV/ref=sr_1_10?crid=2M096C61O4MLT&keywords=bags&qid=1675253937&sprefix=ba%2Caps%2C283&sr=8-10&th=1"

header = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}
response = requests.get(url=TABULAR_URL, headers=header).text

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

print(asin)
print(description)
print(manufacturer)