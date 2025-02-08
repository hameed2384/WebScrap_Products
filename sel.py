import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Initialize session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def scrape_product_data(product_number):
    base_url = f'https://www.econox.nl/nl_NL/p/thermoduct-9mm-beugel-450mm-pctd450/{product_number}/'
    try:
        response = session.get(base_url, headers=headers, allow_redirects=True)
        if response.status_code != 200:
            print(f"Product {product_number} does not exist. Skipping.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find('h1', string="Sorry, de pagina die u probeert te bereiken bestaat helaas niet.")
        if error_message:
            print(f"Product {product_number} does not exist (unavailable message). Skipping.")
            return None

        # Debug: Print product number and URL
        print(f"Scraping Product {product_number}: URL - {response.url}")

        # Extract product details with additional checks
        product_name_tag = soup.find('div', {'class': 'pdp-meta'}).find('h1') if soup.find('div', {'class': 'pdp-meta'}) else None
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else "No name available"
        
        product_brand_tag = soup.find('div', {'class': 'pdp-meta__subtitle'}).find('a') if soup.find('div', {'class': 'pdp-meta__subtitle'}) else None
        product_brand = product_brand_tag.get_text(strip=True) if product_brand_tag else "No brand available"
        
        features_list = soup.find('div', {'class': 'product-addons'}).find('ul', {'class': 'list--checked'}) if soup.find('div', {'class': 'product-addons'}) else None
        features = [li.get_text(strip=True) for li in features_list.find_all('li')] if features_list else []
        
        description_div = soup.find('div', {'class': 'pdp-description'}) if soup.find('div', {'class': 'pdp-description'}) else None
        description = description_div.get_text(strip=True) if description_div else "No description available."

        # Extract specifications
        specifications_wrapper = soup.find('div', {'class': 'pdp-specifications__item-wrapper'}) if soup.find('div', {'class': 'pdp-specifications__item-wrapper'}) else None
        specifications = []
        if specifications_wrapper:
            table_rows = specifications_wrapper.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True).replace(":", "")
                    value = cells[1].get_text(strip=True)
                    specifications.append(f"{key}: {value}")
        
        # Combining specifications with a separator (| in this case)
        specifications = " | ".join(specifications) if specifications else "No specifications available"

        return {
            'Product Number': product_number,
            'Name': product_name,
            'Brand': product_brand,
            'Features': "; ".join(features),
            'Description': description,
            'Specifications': specifications,  # Correct column name
            'URL': response.url
        }

    except Exception as e:
        # Enhanced debugging for specific product numbers
        print(f"Error fetching product {product_number}: {e}")
        # Optionally, print the full HTML response to debug the issue further for that product
        with open(f"debug_product_{product_number}.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        return None


# Function to write data to CSV
def write_to_csv(data, file_name='econox_products.csv'):
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Product Number', 'Name', 'Brand', 'Features', 'Description', 'Specifications', 'URL'])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

# Main function to loop through product numbers and scrape data
def main(start_product_number, end_product_number):
    for product_number in range(start_product_number, end_product_number):
        product_data = scrape_product_data(product_number)
        if product_data:
            write_to_csv(product_data)
            print(f"Successfully scraped product {product_number}")
        time.sleep(1)  # Delay to prevent being flagged as a bot

# Run the script
if __name__ == "__main__":
    main(start_product_number=0, end_product_number=40)
