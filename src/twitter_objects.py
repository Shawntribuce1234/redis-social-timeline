'''
This module defines the objects that I will be using in Homework 1
'''
class TWEET:

    def __init__(self, user_id, tweet_text):
        self.user_id = user_id
        self.tweet_text = tweet_text

class FOLLOWS:

    def __init__(self, follower_id, followee_id):
        self.follower_id = follower_id
        self.followee_id = followee_id



