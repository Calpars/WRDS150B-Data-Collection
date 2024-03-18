
import requests
from bs4 import BeautifulSoup
import pandas as pandas
url = 'https://www.cbc.ca/news/canada/new-brunswick/nuclear-vp-leaving-nb-power-1.6975931'; # Replace this with the URL of the website you want to scrape

response = requests.get(url)
# Check if the request was successful
if response.status_code == 200:
    html_content = response.content
else:
    print("Failed to fetch the website.")
    exit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the text elements (e.g., paragraphs, headings, etc.) you want to scrape

text_elements = soup.find_all('p')
# Extract the text from each element and concatenate them into a single string
scraped_text = ' '.join(element.get_text() for element in text_elements)
x = scraped_text.removesuffix('  Audience Relations, CBC P.O. Box 500 Station A Toronto, ON  Canada, M5W 1E6  Toll-free (Canada only):  1-866-306-4636 It is a priority for CBC to create products that are accessible to all in Canada including people with visual, hearing, motor and cognitive challenges. Closed Captioning and Described Video is available for many CBC shows offered on CBC Gem.')
print(x)