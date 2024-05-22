import requests
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import socks
import socket
import re
import nltk
from nltk.corpus import stopwords
import spacy

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

# Configure SOCKS5 proxy with Tor
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9050)
socket.socket = socks.socksocket

# Define the proxy settings for requests to use Tor's SOCKS5 proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

# Function to preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters using a regular expression
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove numbers using a regular expression
    text = re.sub(r'\d+', '', text)
    
    # Tokenize the text using spaCy
    doc = nlp(text)
    
    # Remove stop words using NLTK
    stop_words = set(stopwords.words('english'))
    tokens = [token.text for token in doc if token.text not in stop_words]
    
    # Join the tokens back into a single string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

# Function to scrape a single onion site
def scrape_onion_site(url):
    try:
        # Make a request using the proxy settings
        response = requests.get(url, proxies=proxies, timeout=20)
        if response.status_code == 200:
            # Parse the HTML and extract the text content
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            
            # Preprocess the text using the preprocess_text function
            preprocessed_text = preprocess_text(text)
            
            print(f"Successfully scraped and preprocessed {url}")
            # Return the preprocessed text
            return preprocessed_text
        else:
            print(f"Failed to scrape {url}: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

# Function to scrape multiple onion sites concurrently and store data in a CSV file
def scrape_and_store_in_csv(urls, csv_filename):
    # List to store preprocessed data
    preprocessed_data_list = []
    
    # Create a ThreadPoolExecutor to handle multiple requests concurrently
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit scraping tasks for each URL
        future_to_url = {executor.submit(scrape_onion_site, url): url for url in urls}

        # Collect results from the futures
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                # Get the result (preprocessed text) from the future
                preprocessed_text = future.result()
                
                if preprocessed_text:
                    # Store the preprocessed data in the list
                    preprocessed_data_list.append((url, preprocessed_text))
                    print(f"Processing data from {url}")
            except Exception as exc:
                print(f"Error processing data from {url}: {exc}")

    # Store preprocessed data in a CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Preprocessed Text'])
        for url, preprocessed_text in preprocessed_data_list:
            writer.writerow([url, preprocessed_text])
    
    print(f"Preprocessed data has been stored in {csv_filename}")

# Allow user to input a list of onion sites and a CSV filename
user_input = input("Enter the onion URLs (comma-separated): ")
urls = user_input.split(',')

# Strip any leading/trailing spaces from each URL
urls = [url.strip() for url in urls]

csv_filename = input("Enter the CSV filename to store the data: ")

# Scrape the onion sites concurrently and store data in a CSV file
scrape_and_store_in_csv(urls, csv_filename)

print("\nThe scraping and storage process is complete.")

