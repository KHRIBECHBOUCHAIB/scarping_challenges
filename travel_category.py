import requests
from bs4 import BeautifulSoup

# Example category URL: Travel
category_url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

# Fetch the HTML content of the category page
response = requests.get(category_url)

# Step 1: Check if the request was successful
if response.status_code == 200:
    # Parse the HTML using 'html.parser' with explicit encoding
    response.encoding = 'utf-8'  # Set the correct encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 2: Find all book elements
    books = soup.find_all('article', class_='product_pod')

    # Step 3: Extract and print the title and price for each book
    for book in books:
        # Extract the title of the book
        title = book.h3.a['title']

        # Extract the price of the book and sanitize it
        price_text = book.find('p', class_='price_color').text.strip()
        price_text = price_text.encode('ascii', 'ignore').decode('ascii')  # Remove any non-ASCII characters
        price = float(price_text.replace('£', '').strip())  # Remove the "£" symbol and convert to float

        # Print book details
        print(f"Title: {title}, Price: £{price}")

else:
    print(f"Failed to retrieve page at {category_url}, status code: {response.status_code}")
