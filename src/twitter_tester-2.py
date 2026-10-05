"""
File used to test the TwitterAPI class and its methods.
It includes code to authenticate, pre-load the follows and tweets tables,
and retrieve a user's home timeline.
"""
import random
import pandas as pd
import time
from twitter_redis import TwitterRedisAPI
from twitter_objects import TWEET, FOLLOWS


def main():

    # Authenticate
    api = TwitterRedisAPI(host='localhost', port=6379)

   # Pre-load the follows table
    df_follows = pd.read_csv("/Users/shawntribuce/PycharmProjects/DS4300/Homework_1/hw1_data/follows.csv")

    # Replaced itterrows() to itertuples() for faster iteration
    for row in df_follows.itertuples(index=False):
        follow = FOLLOWS(int(row.USER_ID), int(row.FOLLOWS_ID))
        api.log_follow(follow)



    # # Pre-load the tweets table
    df_tweets = pd.read_csv("/Users/shawntribuce/PycharmProjects/DS4300/Homework_1/hw1_data/tweet.csv")

    start = time.time()  # Start the timer
    for _, row in df_tweets.iterrows():
         tweet = TWEET(row["USER_ID"], row["TWEET_TEXT"]) # Create a TWEET object using the data from the row
         api.log_tweet(tweet) # Log the tweet into the database using the API
    end = time.time() # End the timer

    total_tile = end - start # Calculate the total time taken to insert the tweets
    tweets_per_second = len(df_tweets) / total_tile # Calculate the number of tweets inserted per second
    print(f"Time taken to insert {len(df_tweets)}, tweets per second: {tweets_per_second}")



    # Testing home timeline retrieval
    num_requests = 1000
    start = time.time() # Start the timer

    # Simulate multiple requests to get home timelines for random users
    for _ in range(num_requests):
        user_id = random.randint(1, 10000) # Assigning random user_id
        timeline = api.get_home_timeline(user_id)

    end = time.time() # End the timer

    total_time = end - start
    timelines_per_second = num_requests / total_time
    print(f"Timelines per second: {timelines_per_second}")

if __name__ == '__main__':
    main()