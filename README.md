# Web Scraping Project: Books, Quotes, and Advanced Quote Search

This project consists of three web scraping modules that scrape data from different websites using similar dependencies:

1. **Books Scraper** - Scrapes book information from `books.toscrape.com`.
2. **Quotes Scraper** - Scrapes quotes from `quotes.toscrape.com` after logging in.
3. **Advanced Quote Search** - Scrapes quotes from `quotes.toscrape.com` using a more advanced search functionality, allowing searches by author and tags.

All scripts make use of Python's `requests` library for making HTTP requests and `BeautifulSoup` for parsing HTML. The project is gathered into one repository because all modules share similar dependencies.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Books Scraper](#books-scraper)
  - [Quotes Scraper](#quotes-scraper)
  - [Advanced Quote Search](#advanced-quote-search)
- [Dependencies](#dependencies)

## Project Overview

This project was created to demonstrate web scraping skills using Python. It includes:
- **Scraping books**: Collects book titles and prices from various categories on `books.toscrape.com`.
- **Scraping quotes**: Connects to `quotes.toscrape.com` with login credentials to extract quotes, authors, and tags from multiple pages.
- **Advanced quote search**: Searches quotes on `quotes.toscrape.com` by author and tag, using custom search capabilities.

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

### Advanced Quote Search:
- Searches quotes by a specific author with a specific tag.
- Uses advanced form handling to interact with the search functionality on the website.
- Extracts quotes, authors, and tags from search results.

## Installation

Make sure you have Python 3.6 or newer installed on your machine. Clone the repository and install the required dependencies.

```sh
# Clone the repository
git clone https://github.com/yourusername/scraping_challenges.git
# Install the required dependencies
pip install -r requirements.txt
