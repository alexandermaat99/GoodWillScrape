import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://books.toscrape.com/"
response = requests.get(url)

# parsing the HTML content

soup = BeautifulSoup(response.text, 'html.parser') 
books = soup.find_all('article', class_='product_pod')
book_data = []

for book in books:
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text
    price = price.replace('Â£', '£')    
    book_data.append([title, price])   

df = pd.DataFrame(book_data)
df.to_csv('books.csv', index=False, header=['Title', 'Price'])

