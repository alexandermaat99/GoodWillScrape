import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

#what the user is searching for
# searchFor = input("What would you like to search for? ")

searching_list = ["contax", "mamiya", "nikon l35"]

#how many resposnes the user wants to see  
num_responses = 100
# numOfResponses = 100

#convert the number of responses to a string
responses = str(num_responses)

all_data = []

for i in searching_list:
    searchFor = i

    #url to scrape
    url = "https://www.goodwillfinds.com/search/?q=" + searchFor + "&sz="+ responses + "&start=0"
    response = requests.get(url)

    # parsing the HTML content

    soup = BeautifulSoup(response.text, 'html.parser') 

    products = soup.find_all('article', class_='b-product_tile')

    # List to store product data
    # product_data = []

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
        all_data.append({"search":searchFor,"Title": title, "Price": price, "Sale": sale, "URL": url})


# Convert the list to a pandas DataFrame
df = pd.DataFrame(all_data)
today_date = pd.Timestamp.now().strftime("%m-%d-%Y")

# Save the DataFrame to a CSV file
df.to_csv(f"dailyScrape.csv", index=False)


# Save the DataFrame to a JSON file
# df.to_json('{today_date} + {searchFor} + {numOfResponses} + '_goodwill_products.json'', orient='records')
print("Data has been saved to goodwill_products.csv and goodwill_products.json.")



def send_email(file_path):
    # Correctly read the password from the 'password.txt' file
    with open('idk.txt', 'r') as file:
        password = file.read().strip()

    from_email = "aamaat99@gmail.com"
    to_email = "aamaat99@gmail.com"
    subject = "Daily Goodwill Scrape"
    body = "Here is the daily scrape of Goodwill products."

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
        msg.attach(part)

    # Connect to the server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

send_email('dailyScrape.csv')
print(f"Data has been saved to {'dailyScrape.csv'} and emailed.")