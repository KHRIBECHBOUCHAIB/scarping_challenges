import requests
from bs4 import BeautifulSoup
import time
import json
import os

def fetch_random_quote(session):
    """
    Fetches a random quote from the website.
    
    Args:
        session (requests.Session): The session object to make requests.
        
    Returns:
        dict or None: A dictionary containing the quote text, author, and tags if successful; otherwise, None.
    """
    url = "https://quotes.toscrape.com/random"
    try:
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            quote_div = soup.find('div', class_='quote')
            if quote_div:
                # Attempt to find the quote text in 'span.text' or 'span.content'
                text_tag = quote_div.find('span', class_='text') or quote_div.find('span', class_='content')
                # Attempt to find the author in 'small.author' or 'span.author'
                author_tag = quote_div.find('small', class_='author') or quote_div.find('span', class_='author')
                
                # Extract text and author if tags are found
                text = text_tag.get_text(strip=True) if text_tag else "No text found"
                author = author_tag.get_text(strip=True) if author_tag else "No author found"
                # Extract all tags associated with the quote
                tags = [tag.get_text(strip=True) for tag in quote_div.find_all('a', class_='tag')]
                
                return {'text': text, 'author': author, 'tags': tags}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None

def save_quotes_to_file(quotes, output_dir='output', filename='quotes.json'):
    """
    Saves the collected quotes to a JSON file in the specified directory.
    
    Args:
        quotes (list): A list of dictionaries containing quote details.
        output_dir (str): The directory where the JSON file will be saved.
        filename (str): The name of the JSON file.
        
    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Define the full path to the output file
    output_path = os.path.join(output_dir, filename)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)
        print(f"\nQuotes have been successfully saved to '{output_path}'")
    except IOError as e:
        print(f"Failed to save quotes to file: {e}")

def main():
    """
    Main function to execute the scraping process.
    
    Args:
        None
        
    Returns:
        None
    """
    base_url = "https://quotes.toscrape.com/"
    total_unique_quotes = 100  # Known number of unique quotes on the site
    collected_quotes = {}
    attempt = 0
    max_attempts = 10000  # Safety limit to prevent infinite loops
    
    # Define output directory and filename
    output_dir = 'output'
    output_filename = 'quotes.json'
    
    with requests.Session() as session:
        while len(collected_quotes) < total_unique_quotes and attempt < max_attempts:
            quote = fetch_random_quote(session)
            if quote:
                unique_id = quote['text']
                if unique_id not in collected_quotes:
                    collected_quotes[unique_id] = quote
                    print(f"Collected {len(collected_quotes)}/{total_unique_quotes}: \"{quote['text']}\" - {quote['author']}")
            attempt += 1
            time.sleep(0.5)  # Pause between requests to be polite to the server
    
    # Check if all unique quotes were collected
    if len(collected_quotes) == total_unique_quotes:
        print("\nSuccessfully collected all unique quotes!")
    else:
        print(f"\nStopped after {attempt} attempts. Collected {len(collected_quotes)} unique quotes.")
    
    # Save the collected quotes to a file
    quotes_list = list(collected_quotes.values())
    save_quotes_to_file(quotes_list, output_dir, output_filename)

if __name__ == "__main__":
    main()
