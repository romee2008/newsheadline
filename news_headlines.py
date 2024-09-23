import tweepy
import requests
import time
from os import environ
from bs4 import BeautifulSoup
from datetime import datetime
import os
import sys

consumer_key1 = environ['CONSUMER_KEY']
consumer_secret_key1 = environ['CONSUMER_SECRET_KEY']
access_token1 = environ['ACCESS_TOKEN']
access_token_secret1 = environ['ACCESS_TOKEN_SECRET']

client = tweepy.Client(consumer_key=consumer_key1,
                        consumer_secret=consumer_secret1,
                        access_token=access_token1,
                        access_token_secret=access_token_secret1)





# Load the unique counter from a file
def load_unique_counter(filename='unique_counter.txt'):
    if not os.path.exists(filename):
        return 1  # Start from 1 if the file doesn't exist
    
    with open(filename, 'r') as file:
        content = file.read().strip()
        return int(content) if content else 1  # Return 1 if the content is empty

# Save the unique counter to a file
def save_unique_counter(counter, filename='unique_counter.txt'):
    with open(filename, 'w') as file:
        file.write(str(counter))

# Fetch BBC News Headlines
def fetch_bbc_headlines():
    url = 'https://www.forexlive.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract headlines (This might vary based on the page structure)
    headlines = [headline.text.strip() for headline in soup.find_all('h3')]  # Adjust selector as per the structure
    return list(dict.fromkeys(headlines))[:1]  # Remove duplicates, take top 20

# Function to tweet headlines
def tweet_headlines():
    headlines = fetch_bbc_headlines()
    unique_number_counter = load_unique_counter()

    # Prepare the tweet text
    tweet_text = "Financial Summary\n" + time.strftime('%A, %B %d, %Y') + "\n\n"
    character_limit = 280
    count = unique_number_counter
    
    for headline in headlines:
        line = f"{count}. {headline}\n"
        
        # If the current tweet exceeds the character limit, tweet it and start a new one
        if len(tweet_text + line) > character_limit:
            try:
                client.create_tweet(text=tweet_text)
                print(f'Tweeted: {tweet_text}')
                time.sleep(10)  # Wait before next tweet
            except tweepy.TweepyException as e:
                print(f'Error: {e}')
            
            # Reset tweet text
            tweet_text = "Financial Summary\n" + time.strftime('%A, %B %d, %Y') + "\n\n"
        
        tweet_text += line
        count += 1  # Increment the unique number counter
    
    # Tweet any remaining headlines
    if tweet_text.strip():
        try:
            client.create_tweet(text=tweet_text)
            print('tweeted')
        except tweepy.TweepyException as e:
            print(f'Error: {e}')

    # Save the updated counter
    save_unique_counter(count)

if __name__ == "__main__":
    tweet_headlines()







