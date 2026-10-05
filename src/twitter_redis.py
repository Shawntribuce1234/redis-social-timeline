'''
Using a hashmap to store each tweet's data and a list to keep track of each user's home timeline
to give each user their own timeline based on their following
'''

import redis
from datetime import datetime
from twitter_objects import TWEET, FOLLOWS


class TwitterRedisAPI:

    def __init__(self, host="localhost", port=6379, db=0):
        # Make a connection
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.r.flushall()  # Clear the database before starting

    def log_follow(self, follow):
        # Store follow relationship as a value in folowers:{followee_id} set
        self.r.sadd(f"followers:{follow.followee_id}", follow.follower_id) # sadd ensures no duplicates

    def log_tweet(self, tweet):
        # Set tweet id to auto increment
        tweet_id = self.r.incr("tweet:counter")

        # Setting up the hashmap for each tweet value
        self.r.hset(f"tweet:{tweet_id}", mapping={
            "user_id":    tweet.user_id,
            "tweet_text": tweet.tweet_text,
            "tweet_ts":   datetime.now().isoformat()
        })

        # Create buckets and store the tweet id in the appropriate bucket based on the timestamp
        followers = self.r.smembers(f"followers:{tweet.user_id}")
        for follower_id in followers:
            self.r.lpush(f"timeline:{follower_id}", tweet_id)  # lpush lists the most recent first
            self.r.ltrim(f"timeline:{follower_id}", 0, 999)    # cap list at 1000 entries

    def get_home_timeline(self, user_id):
        # Get the 10 most recent tweet IDs from this user's timeline list
        tweet_ids = self.r.lrange(f"timeline:{user_id}", 0, 9)

        # For each tweet ID fetch the hashmap convert to a tweet object
        tweets = []
        for tweet_id in tweet_ids:
            data = self.r.hgetall(f"tweet:{tweet_id}")
            if data:
                tweets.append(TWEET(data["user_id"], data["tweet_text"]))

        return tweets