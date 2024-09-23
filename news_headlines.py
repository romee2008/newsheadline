from dotenv import load_dotenv
load_dotenv()
import tweepy
import requests
import time
import sys
from os import environ
from bs4 import BeautifulSoup
from datetime import datetime
import os

consumer_key1 = environ['CONSUMER_KEY']
consumer_secret_key1 = environ['CONSUMER_SECRET_KEY']
access_token1 = environ['ACCESS_TOKEN']
access_token_secret1 = environ['ACCESS_TOKEN_SECRET']

client = tweepy.Client(consumer_key=consumer_key1,
                        consumer_secret=consumer_secret_key1,
                        access_token=access_token1,
                        access_token_secret=access_token_secret1)

# Fetch BBC News Headlines
def fetch_bbc_headlines():
    url = 'https://www.forexlive.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract headlines (This might vary based on the page structure)
    headlines = [headline.text.strip() for headline in soup.find_all('h3')]  # Adjust selector as per the structure
    return list(dict.fromkeys(headlines))[:20]  # Remove duplicates, take top 20

# Load previously tweeted headlines
def load_tweeted_headlines(filename='tweeted_headlines.txt'):
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Save a new headline to the log file
def save_tweeted_headline(headline, filename='tweeted_headlines.txt'):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{headline}\n")

# Function to tweet headlines
def tweet_headlines():
    headlines = fetch_bbc_headlines()
    tweeted_headlines = load_tweeted_headlines()

    # Filter out headlines that have already been tweeted
    new_headlines = [headline for headline in headlines if headline not in tweeted_headlines]
    
    if not new_headlines:
        print("No new headlines to tweet.")
        return

    tweet_text = "Financial Summary\n" + time.strftime('%A, %B %d, %Y') + "\n\n"
    character_limit = 280
    count = 1
    
    for headline in new_headlines:
        line = f"{count}. {headline}\n"
        
        # If the current tweet exceeds the character limit, tweet it and start a new one
        if len(tweet_text + line) > character_limit:
            try:
                client.create_tweet(text=tweet_text)
                print(f'Tweeted: {tweet_text}')
                time.sleep(10)
            except tweepy.TweepyException as e:
                print(f'Error: {e}')
            
            # Reset tweet text
            tweet_text = "Financial Summary\n" + time.strftime('%A, %B %d, %Y') + "\n\n"
        
        tweet_text += line
        save_tweeted_headline(headline)  # Save the tweeted headline
        count += 1
    
    # Tweet any remaining headlines
    if tweet_text.strip():
        try:
            client.create_tweet(text=tweet_text)
            print(f'Tweeted: {tweet_text}')
        except tweepy.TweepyException as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    tweet_headlines()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

response = requests.get('https://www.ft.com', headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
