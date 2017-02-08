#! /usr/bin/env python3

import tweepy
import socket
import sys

host = '172.29.56.50'
port = 50000
size = 1024
s = None

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
except socket.error as message:
    if s:
        s.close()
    print ("Unable to open socket: " + str(message))
    sys.exit(1)

auth = tweepy.OAuthHandler('M97QpyCyGJjIavBMODxvhIEVA', '2nEZhV1fb2DAwMxz9qvIt7ApVxMKXZKvcnjlIBoKNSo7vZbGNf')
auth.set_access_token('827585219586879488-hXLr5DyfxyJkp61HVtLMHTn7dSfXqYr', 'hCWHmF3EKoXlt1ExEUA0j47JTNBfjGwk8weOOgWdoZ3rp')

api = tweepy.API(auth)

""" Downloads home timeline tweets and prints each one out to the console """
# public_tweets = api.home_timeline()
#
# for tweet in public_tweets:
#     print (tweet.text)

""" Calls a function to tweet """
# api.update_status('This is a tweet from python boyz!')

""" Streaming with tweepy - Create a StreamListener class """
class MyStreamListener(tweepy.StreamListener):

     # This method overrides the on_data method
    def on_status(self, status):
        print(status.text)

        try:
            # Sends the tweet to the server and receives the answer
            s.send(status.text.encode())
            data = s.recv(size)
            print(data.decode())
        except socket.error as message:
            if s:
                s.close()
            print ("Unable to connect to socket: " + str(message))

    def on_error(selfself, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

# Create a stream
myStreamListener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Start a stream - async makes the stream run on a new thread
myStream = stream.userstream()
