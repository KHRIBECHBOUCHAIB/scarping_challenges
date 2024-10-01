import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def extract_categories(base_url):
    response = requests.get(base_url)
    category_links = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        categories_section = soup.find('div', class_='side_categories')
        if categories_section:
            categories = categories_section.find_all('a')
            for category in categories:
                category_name = category.text.strip()
                href = category.get('href')
                category_url = urljoin(base_url, href)
                category_links[category_name] = category_url

        # Print extracted categories
        print("Categories extracted:")
        for name, link in category_links.items():
            print(f" - {name}: {link}")
    else:
        print(f"Failed to retrieve the main page. Status code: {response.status_code}")

    return category_links

def scrape_books_in_category(category_url):
    all_books = []
    current_url = category_url
    page_number = 1

    while current_url:
        print(f"Fetching page {page_number}: {current_url}")
        response = requests.get(current_url)

        if response.status_code != 200:
            print(f"Failed to retrieve page at {current_url}, status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all book elements on the current page
        books = soup.find_all('article', class_='product_pod')

        if not books:
            print(f"No books found on page {page_number} of {category_url}")
            break

        print(f"Found {len(books)} books on page {page_number}")

        for book in books:
            # Extract the title of the book
            title = book.h3.a['title']

            # Extract the price of the book and sanitize it
            price_text = book.find('p', class_='price_color').text.strip()
            price_text = price_text.encode('ascii', 'ignore').decode('ascii')  # Remove any non-ASCII characters
            try:
                price = float(price_text.replace('£', '').strip())  # Remove the "£" symbol and convert to float
            except ValueError:
                print(f"Could not convert price: {price_text} for book: {title}")
                price = 0.0

            # Append title and price to the book list
            all_books.append((title, price))

        # Check if there is a next page
        next_button = soup.find('li', class_='next')
        if next_button:
            next_href = next_button.find('a')['href']
            current_url = urljoin(current_url, next_href)
            page_number += 1
            time.sleep(1)  # Add delay to avoid overwhelming the server
        else:
            current_url = None  # No more pages

    return all_books

def calculate_statistics(books):
    total_books = len(books)
    if total_books == 0:
        average_price = 0.0
    else:
        total_price = sum(price for _, price in books)
        average_price = round(total_price / total_books, 2)
    return total_books, average_price

# Main script to extract categories, scrape books, and calculate statistics
if __name__ == "__main__":
    base_url = "https://books.toscrape.com/"
    category_links = extract_categories(base_url)

    # Iterate through each category and scrape books
    for category_name, category_link in category_links.items():
        # Skip the "Books" root category which contains all books
        if category_name.lower() == 'books':
            continue
        print(f"\nProcessing category: {category_name}")
        books = scrape_books_in_category(category_link)
        
        # Calculate statistics
        total_books, average_price = calculate_statistics(books)
        
        # Display the results
        print(f" - Number of Books: {total_books}")
        print(f" - Average Price: £{average_price}")
        
        # Optionally, print all books
        for title, price in books:
            print(f"   - Title: {title}, Price: £{price}")
