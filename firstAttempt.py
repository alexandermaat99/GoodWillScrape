import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.goodwillfinds.com/search/?q=camera&sz=200&start=0"
response = requests.get(url)

# parsing the HTML content

soup = BeautifulSoup(response.text, 'html.parser') 

products = soup.find_all('article', class_='b-product_tile')

# List to store product data
product_data = []

for product in products:
    # Extract the product name
    title_element = product.find('a', class_='b-product_tile-title_link')
    title = title_element.text.strip() if title_element else "N/A"
    
    # Extract the product price
    price_element = product.find('span', class_='b-price-item')
    price = price_element.text.strip() if price_element else "N/A"

    sale_element = product.find('span', class_='b-price-discount')
    sale = sale_element.text.strip() if sale_element else "N/A"
    
    # Append the product data to the list
    product_data.append({"Title": title, "Price": price, "Sale": sale})

# Convert the list to a pandas DataFrame
df = pd.DataFrame(product_data)

# Save the DataFrame to a CSV file
df.to_csv('goodwill_products.csv', index=False)

print("Data has been saved to goodwill_products.csv")