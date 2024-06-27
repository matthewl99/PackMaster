import requests
from bs4 import BeautifulSoup

BASE_URL = "http://example.com/items?page={}"

def scrape_page(page_number):
    """Scrapes a single page and returns items found."""
    response = requests.get(BASE_URL.format(page_number))
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Extracting items assuming they are in <div class="item">
        items = soup.find_all('div', class_='item')
        return [item.text for item in items]
    else:
        return None

def scrape_all_pages():
    """Scrapes all pages until no more items are found."""
    all_items = []
    page_number = 1
    while True:
        items = scrape_page(page_number)
        if items:
            all_items.extend(items)
            page_number += 1
        else:
            break  # No more items found, stop pagination
    return all_items

# Example usage
all_items = scrape_all_pages()
print(all_items)