Product Scraper - README
Description
This script scrapes product data from Econox website and saves the information into a CSV file. The data includes product names, brands, features, descriptions, and specifications.

You can run this as an executable file without the need to set up Python or install dependencies manually. The executable will scrape the products and store the results in a CSV file.

Files Included:
sel.exe (or sel for Mac/Linux): The main executable file that runs the scraper.
requirements.txt: A file listing the Python libraries required to run the script from source code (only needed if you want to run the script directly and not as an executable).
README.md: This file with instructions on how to use the script.
How to Use
Running the Executable:
For Windows:

Simply double-click the sel.exe file.
The script will start scraping data, and the resulting econox_products.csv file will be saved in the same directory as the executable.
For Mac/Linux:

Open a terminal.
Navigate to the folder containing the sel executable.
Run the script by typing:
bash
Copy
Edit
./sel
The script will begin scraping data and generate a CSV file named econox_products.csv in the same directory.
What the Script Scrapes:
Product Name
Brand
Features
Description
Specifications
URL
Customizing the Scraper
You can edit the script to change the range of product numbers to scrape, or modify the scraping logic to suit your needs. If you need to run the script from source code instead of using the executable, follow the instructions below.

Running from Source Code (Optional)
If you prefer to run the script from the source code (e.g., sel.py), follow these steps:

Install Python (version 3.x).

Install the required libraries by running:

bash
Copy
Edit
pip install -r requirements.txt
After installing the dependencies, run the script with:

bash
Copy
Edit
python sel.py
Output
The data will be saved in a CSV file named econox_products.csv. You can open this file using any spreadsheet application (e.g., Excel, Google Sheets).

Troubleshooting
Common Errors:
'NoneType' object has no attribute 'find': This error occurs when the script cannot find a specific HTML element on the product page. It typically happens if the product page layout has changed or the page is unavailable.

Product does not exist: If the script encounters a "Page Not Found" error or a non-existing product URL, it will skip the product and continue with the next.

If you encounter any other issues, feel free to reach out!

License
This project is open-source and free to use. Feel free to modify and distribute it as per your needs.
