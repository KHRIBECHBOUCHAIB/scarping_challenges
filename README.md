# Web Scraping Project: Books, Quotes, and Random Quotes Collection

This project consists of four web scraping modules that scrape data from different websites using similar dependencies:

1. **Books Scraper** - Scrapes book information from `books.toscrape.com`.
2. **Quotes Scraper** - Scrapes quotes from `quotes.toscrape.com` after logging in.
3. **Einstein's Quotes Module** - Searches for quotes by Albert Einstein, filtering based on specific keywords.
4. **Random Quotes Collector** - Scrapes random quotes from `quotes.toscrape.com` and saves them in a JSON file.

All scripts make use of Python's `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML. The project is gathered into one repository because all modules share similar dependencies.


## Project Overview

This project was created to demonstrate web scraping skills using Python. It includes:
- **Scraping books**: Collects book titles and prices from various categories on `books.toscrape.com`.
- **Scraping quotes**: Connects to `quotes.toscrape.com` with login credentials to extract quotes, authors, and tags from multiple pages.
- **Random Quotes Collection**: Extracts random quotes from `quotes.toscrape.com` until a given number of unique quotes are collected.

### Websites Scraped:
- [Books to Scrape](https://books.toscrape.com)
- [Quotes to Scrape](https://quotes.toscrape.com)

## Features

### Books Scraper:
- Extracts categories and scrapes books from each category.
- Calculates the average price of books in each category.
- Saves information including book titles and prices.

### Quotes Scraper:
- Logs into the website using provided credentials.
- Scrapes quotes, authors, and tags.
- Provides answers to simple questions based on the scraped quotes (e.g., first and fifth quote, most frequent tag).

### Einstein's Quotes Module:
- Searches for quotes by Albert Einstein and filters based on specific keywords.
- Extracts quotes that contain the keyword and prints them.

### Random Quotes Collector:
- Scrapes random quotes from `quotes.toscrape.com`.
- Collects up to 100 unique quotes, including their text, author, and tags.
- Saves the collected quotes in a JSON file.

## Installation

Make sure you have Python 3.6 or newer installed on your machine. Clone the repository and install the required dependencies.

```sh
# Clone the repository
git clone https://github.com/yourusername/scraping-challenges.git


# Install the required dependencies
pip install -r requirements.txt
