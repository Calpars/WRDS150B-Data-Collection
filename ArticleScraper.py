
import nltk
#nltk.download('all')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import requests
import time
from bs4 import BeautifulSoup
import pandas as pandas

#URLS = ["Geothermal_URLs.txt", "Nuclear_URLs.txt", "Solar_URLs.txt", "Tidal_URLs.txt", "Wind_URLs.txt"]
#OUTPUTS = ["Geothermal_Output.csv", "Nuclear_Output.csv", "Solar_Output.csv", "Tidal_Output.csv", "Wind_Output.csv"]

URLS_FILE = "Wind_URLs.txt"
OUTPUT_FILE = "Wind_Output.csv"

T_START = time.perf_counter()

def scrape_page(url):
    try:
        response = requests.get(url)
    except:
        quit()
    
    # Check if the request was successful
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to fetch the website.")
        return -1


    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the text elements (e.g., paragraphs, headings, etc.) you want to scrape

    text_elements = soup.find_all('p')
    # Extract the text from each element and concatenate them into a single string
    scraped_text = ' '.join(element.get_text() for element in text_elements)
    scraped_text = scraped_text[:-361]
    return scraped_text

def preprocess_text(text):
    if text == -1:
        return -1
    # Tokenize the text
    tokens = word_tokenize(text.lower())
    # Remove stop words
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    # Join the tokens back into a string
    processed_text = ' '.join(lemmatized_tokens)
    return processed_text


def get_sentiment(text):
    if(text == -1):
        return -10
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    print(scores)
    sent_pos = scores['pos']
    sent_neg = scores['neg']
    if(sent_pos > sent_neg):
        return sent_pos
    return -sent_neg

def write_to_file(sent, date = '2024-03-20'):
    if(sent == -10):
        return -1
    f = open(OUTPUT_FILE, "a")
    data = "{sentiment},{date}"
    f.write(data.format(sentiment = sent, date = date))
    f.close()


def generate_data():
    f = open(URLS_FILE, "r")
    lines = f.readlines()
    f.close()
    for i in range(0, len(lines) + 1, 2):
        lines[i] = lines[i][:-1]
        write_to_file(get_sentiment(preprocess_text(scrape_page(lines[i]))), lines[i+1])
        print(f"{i/2} Articles Analyzed. Time elapsed: {time.perf_counter()-T_START:.4f} seconds.")

generate_data()

