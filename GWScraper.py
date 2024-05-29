import requests
from bs4 import BeautifulSoup
import pandas as pd

#what the user is searching for
searchFor = input("What would you like to search for? ")

#how many resposnes the user wants to see  
numOfResponses = input("How many responses would you like to see? ")
# numOfResponses = 100

#convert the number of responses to a string
responses = str(numOfResponses)


#ask the user if they would like to sort by price
sort = input("Would you like to sort by price? (y/n) ").lower()
if sort == "y":
    sort = "&srule=price-low-to-high"
elif sort == "n":
    sort = ""
else: 
    print("Invalid input. No sorting will be done.")
    sort = ""

#url to scrape
url = "https://www.goodwillfinds.com/search/?q=" + searchFor + "&sz="+ responses + "&start=0" + sort
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
    if price_element:
        price_str = price_element.text.strip()
        # Remove the first 14 characters and convert to float
        try:
            price = float(price_str[14:])
        except ValueError:
            price = "N/A"
    else:
        price = "N/A"

    sale_element = product.find('span', class_='b-price-discount')
    sale = sale_element.text.strip() if sale_element else "N/A"

    # Extract the product URL
    url_element = product.find('a', class_='b-product_tile-title_link')
    url = "https://www.goodwillfinds.com/" + url_element['href'] if url_element else "N/A"
    
    # Append the product data to the list
    product_data.append({"Title": title, "Price": price, "Sale": sale, "URL": url})


# Convert the list to a pandas DataFrame
df = pd.DataFrame(product_data)
today_date = pd.Timestamp.now().strftime("%m-%d-%Y")

# Save the DataFrame to a CSV file
df.to_csv(f"{searchFor}_{today_date}_{numOfResponses}.csv", index=False)


# Save the DataFrame to a JSON file
# df.to_json('{today_date} + {searchFor} + {numOfResponses} + '_goodwill_products.json'', orient='records')
print("Data has been saved to goodwill_products.csv and goodwill_products.json.")

