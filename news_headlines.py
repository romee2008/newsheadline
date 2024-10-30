import tweepy
import requests
import time
from os import environ
from bs4 import BeautifulSoup
import os

# Twitter API Credentials
consumer_key = environ['CONSUMER_KEY']
consumer_secret_key = environ['CONSUMER_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']

client = tweepy.Client(consumer_key=consumer_key,
                        consumer_secret=consumer_secret_key,
                        access_token=access_token,
                        access_token_secret=access_token_secret)

# Load the previously tweeted headlines
def load_tweeted_headlines(filename='tweeted_headlines.txt'):
    if not os.path.exists(filename):
        return set()  # Return an empty set if the file doesn't exist

    with open(filename, 'r') as file:
        return set(line.strip() for line in file.readlines())

# Save the newly tweeted headlines
def save_tweeted_headlines(headlines, filename='tweeted_headlines.txt'):
    try:
        with open(filename, 'w') as file:
            for headline in headlines:
                file.write(headline + '\n')
        print(f"Saved tweeted headlines: {headlines}")
    except Exception as e:
        print(f"Error saving tweeted headlines: {e}")

# Fetch headlines from the specified URL
def fetch_bbc_headlines():
    url = 'https://www.forexlive.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract headlines (Adjust selector as per the page structure)
    headlines = [headline.text.strip() for headline in soup.find_all('h3')]
    return list(dict.fromkeys(headlines))[:3]  # Remove duplicates and take top 3

# Function to tweet headlines
def tweet_headlines():
    previously_tweeted = load_tweeted_headlines()
    headlines = fetch_bbc_headlines()

    if not headlines:
        print("No headlines fetched.")
        return  # Exit if no headlines are available

    new_headlines = [h for h in headlines if h not in previously_tweeted]  # Filter out already tweeted headlines

    if not new_headlines:
        print("No new headlines to tweet.")
        return  # Exit if there are no new headlines

    for headline in new_headlines:
        try:
            client.create_tweet(text=headline)
            print(f'Tweeted: {headline}')
            previously_tweeted.add(headline)  # Add to tweeted headlines
            time.sleep(10)  # Wait before next tweet
        except tweepy.TweepyException as e:
            print(f'Error: {e}')

    save_tweeted_headlines(previously_tweeted)  # Save updated list of tweeted headlines

if __name__ == "__main__":
    while True:
        tweet_headlines()
        time.sleep(1800)  # Sleep for 30 minutes
