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
                        consumer_secret=consumer_secret_key1,
                        access_token=access_token1,
                        access_token_secret=access_token_secret1)

# Function to load the unique counter from a file
def load_unique_counter(filename='unique_counter.txt'):
    if not os.path.exists(filename):
        return 1  # Start from 1 if the file doesn't exist
    
    with open(filename, 'r') as file:
        return int(file.read().strip())

# Function to save the unique counter to a file
def save_unique_counter(counter, filename='unique_counter.txt'):
    with open(filename, 'w') as file:
        file.write(str(counter))

# Load the counter at the start
unique_number_counter = load_unique_counter()

# Update the counter after tweeting
save_unique_counter(unique_number_counter)















# In-memory storage for unique numbers
tweeted_headlines_numbers = set()
unique_number_counter = 1

# User-Agent list
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G950U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36'
]

# Fetch BBC News Headlines
def fetch_bbc_headlines():
    url = 'https://www.forexlive.com'
    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': 'https://www.google.com',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    # Random sleep before making the request
    time.sleep(random.uniform(1, 3))
    
    response = requests.get(url, headers=headers)
    
    # Check response status
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [headline.text.strip() for headline in soup.find_all('h3')]
    return list(dict.fromkeys(headlines))[:1]  # Remove duplicates, take top 20

# Function to tweet headlines
def tweet_headlines():
    global unique_number_counter  # Access the global counter
    headlines = fetch_bbc_headlines()

    tweet_text = "Financial Summary\n" + time.strftime('%A, %B %d, %Y') + "\n\n"
    character_limit = 280
    
    for headline in headlines:
        # Use the current unique number and increment for the next headline
        unique_number = unique_number_counter
        
        # Check if this unique number has already been used
        if unique_number in tweeted_headlines_numbers:
            unique_number_counter += 1  # Increment if already tweeted
            continue  # Skip to the next headline

        line = f"{unique_number}. {headline}\n"

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
        tweeted_headlines_numbers.add(unique_number)  # Save the unique number of the tweeted headline
        unique_number_counter += 1  # Increment the counter for the next tweet
    
    # Tweet any remaining headlines
    if tweet_text.strip():
        try:
            client.create_tweet(text=tweet_text)
            print('tweeted')
        except tweepy.TweepyException as e:
            print(f'Error: {e}')


# Function to load the unique counter from a file
def load_unique_counter(filename='unique_counter.txt'):
    if not os.path.exists(filename):
        return 1  # Start from 1 if the file doesn't exist
    
    with open(filename, 'r') as file:
        return int(file.read().strip())

# Function to save the unique counter to a file
def save_unique_counter(counter, filename='unique_counter.txt'):
    with open(filename, 'w') as file:
        file.write(str(counter))

# Load the counter at the start
unique_number_counter = load_unique_counter()

# Update the counter after tweeting
save_unique_counter(unique_number_counter)













if __name__ == "__main__":
    tweet_headlines()











