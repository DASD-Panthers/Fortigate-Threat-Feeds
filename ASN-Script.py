import requests
import warnings  # Import warnings module
from bs4 import BeautifulSoup

# Function to read URLs from MasterASN-List.txt, ignoring lines starting with #
def read_urls_from_file(file_path):
    urls = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and lines starting with #
                urls.append(line)
    return urls

# Function to scrape content from a URL
def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract content from the webpage
        content = soup.get_text()
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

# Function to scrape content from all URLs and write to SSLVPN-ASN-Blocks.txt
def scrape_and_export(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in urls:
            content = scrape_content(url)
            if content:
                file.write(f"=== {url} ===\n\n")
                file.write(content)
                file.write("\n\n")

# Main function
if __name__ == "__main__":
    input_file = "MasterASN-List.txt"
    output_file = "SSLVPN-ASN-Blocks.txt"
    urls = read_urls_from_file(input_file)

    # Suppress Beautiful Soup warnings
    warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

    scrape_and_export(urls, output_file)
    print(f"Scraped content has been exported to {output_file}")
