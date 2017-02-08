#! /usr/bin/env python3

import tweepy
import socket
import sys

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
        hashtag = status.text.split("#")
        question = hashtag[1].split('_')[1].strip("\"")

        print("\nTweet: " + status.text)
        print("IP, Port: " + hashtag[1].split('_')[0])
        print("Question: " + question)

        host = hashtag[1].split('_')[0].split(':')[0]
        port = int(hashtag[1].split('_')[0].split(':')[1])
        size = 1024
        s = None

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
        except socket.error as message:
            if s:
                s.close()
            print("Unable to open socket: " + str(message))
            sys.exit(1)

        try:
            s.send(question.encode())
            data = s.recv(size)
            s.close()
            print("Answer: " + data.decode())
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
