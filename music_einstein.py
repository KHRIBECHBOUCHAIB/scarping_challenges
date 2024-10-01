import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_viewstate(soup):
    """
    Extracts the value of the __VIEWSTATE hidden field from the form.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
        
    Returns:
        str: The value of the __VIEWSTATE field or an empty string if not found.
    """
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})
    if viewstate:
        return viewstate.get('value', '')
    return ''

def search_quote(base_url, author, tag):
    """
    Searches for quotes by a specific author with a specific tag.
    
    Args:
        base_url (str): The base URL of the website.
        author (str): The name of the author to search for.
        tag (str): The tag associated with the quote.
        
    Returns:
        list: A list of dictionaries containing quote text, author, and tags.
    """
    search_url = urljoin(base_url, "search.aspx")
    filter_url = urljoin(base_url, "filter.aspx")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Define headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': search_url
    }
    
    # Perform a GET request to access the search form
    initial_response = session.get(search_url, headers=headers)
    if initial_response.status_code != 200:
        print(f"Error accessing the search page: {initial_response.status_code}")
        return []
    
    # Parse the HTML content to extract __VIEWSTATE
    soup = BeautifulSoup(initial_response.text, 'html.parser')
    viewstate = get_viewstate(soup)
    
    if not viewstate:
        print("Unable to find the __VIEWSTATE field.")
        return []
    
    # Prepare the payload for the POST request
    payload = {
        'author': author,
        'tag': tag,
        'submit_button': 'Search',
        '__VIEWSTATE': viewstate
    }
    
    # Submit the form with a POST request to filter.aspx
    post_response = session.post(filter_url, data=payload, headers=headers)
    
    if post_response.status_code != 200:
        print(f"Error submitting the form: {post_response.status_code}")
        return []
    
    # Parse the response to extract quotes
    post_soup = BeautifulSoup(post_response.text, 'html.parser')
    quotes = extract_quotes(post_soup)
    
    return quotes

def extract_quotes(soup):
    """
    Extracts quotes, authors, and tags from the parsed HTML content.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
        
    Returns:
        list: A list of dictionaries containing quote text, author, and tags.
    """
    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        # Attempt to find the quote text in either 'span.text' or 'span.content'
        text_tag = quote.find('span', class_='text')
        if not text_tag:
            text_tag = quote.find('span', class_='content')
        
        text = text_tag.get_text(strip=True) if text_tag else None
        
        # Attempt to find the author in either 'small.author' or 'span.author'
        author_tag = quote.find('small', class_='author')
        if not author_tag:
            author_tag = quote.find('span', class_='author')
        
        author_name = author_tag.get_text(strip=True) if author_tag else None
        
        # Extract all tags associated with the quote
        tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
        
        quotes.append({'text': text, 'author': author_name, 'tags': tags})
    return quotes

def answer_specific_question(quotes, author_name, keyword):
    """
    Filters the quotes to find the unique quote by the specified author containing the keyword.
    
    Args:
        quotes (list): A list of dictionaries containing quote details.
        author_name (str): The name of the author to filter by.
        keyword (str): The keyword to search for within the quote text.
        
    Returns:
        None
    """
    # Filter quotes by author and keyword in text
    filtered_quotes = [
        quote for quote in quotes 
        if quote['author'] == author_name and quote['text'] and keyword.lower() in quote['text'].lower()
    ]
    
    if len(filtered_quotes) == 1:
        print(f"The unique quote by {author_name} on music is:")
        print(f"\"{filtered_quotes[0]['text']}\"")
    elif len(filtered_quotes) > 1:
        print(f"There are {len(filtered_quotes)} quotes by {author_name} containing the word '{keyword}':")
        for i, quote in enumerate(filtered_quotes, 1):
            print(f"{i}. \"{quote['text']}\"")
    else:
        print(f"No quotes by {author_name} containing the word '{keyword}' were found.")

def main():
    """
    The main function to execute the script.
    
    Args:
        None
        
    Returns:
        None
    """
    base_url = "https://quotes.toscrape.com/"
    
    # Search parameters
    author = "Albert Einstein"
    tag = "music"  # Use 'music' as the tag
    
    # Perform the search
    quotes = search_quote(base_url, author, tag)
    
    # Display the result
    answer_specific_question(quotes, author_name=author, keyword=tag)

if __name__ == "__main__":
    main()
