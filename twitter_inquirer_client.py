#! /usr/bin/env python3

import tweepy
import socket
import sys
import pickle
import hashlib
import json

# Twitter authentication
auth = tweepy.OAuthHandler('M97QpyCyGJjIavBMODxvhIEVA', '2nEZhV1fb2DAwMxz9qvIt7ApVxMKXZKvcnjlIBoKNSo7vZbGNf')
auth.set_access_token('827585219586879488-hXLr5DyfxyJkp61HVtLMHTn7dSfXqYr',
                      'hCWHmF3EKoXlt1ExEUA0j47JTNBfjGwk8weOOgWdoZ3rp')

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    # This method overrides the on_data method
    def on_status(self, status):
        try:
            # Parse tweet
            screen_name = status.user.screen_name
            hashtag = status.text.split('#')
            question = hashtag[1].split('_')[1].strip('"')
            tup = (question, hashlib.md5(question.encode()).digest())

            # Set host and port for socket connection
            host = hashtag[1].split('_')[0].split(':')[0]
            port = int(hashtag[1].split('_')[0].split(':')[1])
            size = 1024
            s = None
        except Exception as e:
            print(e)
            return

        print("\nTweet: " + status.text)
        print("IP, Port: " + host + ", " + str(port))
        print("Question: " + question)

        badresponse = True

        try:
            # Try to connect to socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send(pickle.dumps(tup))

            while badresponse:
                data = s.recv(size)
                tup = pickle.loads(data)

                if tup[0] == "ERROR CODE: 2":
                    # Resend question
                    s.send(pickle.dumps(tup))
                    badresponse = True
                elif tup[1] != hashlib.md5(tup[0].encode()).digest():
                    # Request answer, checksum failed
                    print("Error: checksum failed, requesting resend")
                    s.send("ERROR CODE: 2")
                    badresponse = True
                else:
                    # Checksum valid
                    badresponse = False

            s.close()

            # Iterate through all answers and post status
            for item in json.loads(tup[0]):
                tweet1 = '@' + screen_name + ' #Team02_"' + item + '"'
                tweet2 = '@VTNetApps' + ' #Team02_"' + item + '"'

                # tweet1 = (tweet1[:138] + '..') if (len(tweet1) > 140) else tweet1
                # tweet2 = (tweet2[:138] + '..') if (len(tweet2) > 140) else tweet2

                # Tweet back to original sender
                api.update_status(tweet1)

                # Tweet to VTNetApps
                # api.update_status(tweet2)
        except Exception as e:
            if s:
                s.close()
            print("ERROR: " + str(e))
            return

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def main():
    # Create a stream
    myStreamListener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # Start a stream - async makes the stream run on a new thread
    myStream = stream.userstream(async=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting client...")
        sys.exit(2)
