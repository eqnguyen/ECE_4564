#! /usr/bin/env python3

import tweepy
import socket
import sys, os
import pickle
import hashlib
import json
import re

# Twitter authentication
auth = tweepy.OAuthHandler('M97QpyCyGJjIavBMODxvhIEVA', '2nEZhV1fb2DAwMxz9qvIt7ApVxMKXZKvcnjlIBoKNSo7vZbGNf')
auth.set_access_token('827585219586879488-hXLr5DyfxyJkp61HVtLMHTn7dSfXqYr',
                      'hCWHmF3EKoXlt1ExEUA0j47JTNBfjGwk8weOOgWdoZ3rp')

api = tweepy.API(auth)

# Regex pattern for valid question syntax
pattern = re.compile("@NetAppBoyz #\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}_\".*\"")


# Deletes all tweets on the timeline
def batch_delete():
    for status in tweepy.Cursor(api.user_timeline).items():
        try:
            api.destroy_status(status.id)
        except Exception as inst:
            print("Failed to delete:", status.id)
            print(type(inst))
            print(inst.args)
            print(inst)


# Receives all amounts of data from the server
def recvall(sock):
    buff_size = 1024  # 1 KiB

    # get size of incoming answer
    sizeofmsg = sock.recv(buff_size)

    # get the actual answer
    msg = sock.recv(int(sizeofmsg))
    return msg


class MyStreamListener(tweepy.StreamListener):
    # This method overrides the on_data method
    def on_status(self, status):
        # Check the question for valid syntax
        if not pattern.match(status.text):
            print("Tweet is not a question")
            return

        # Parse tweet
        screen_name = status.user.screen_name
        hashtag = status.text.split('#')
        question = hashtag[1].split('_')[1].strip('"')
        tup = (question, hashlib.md5(question.encode()).digest())

        # Set host and port for socket connection
        host = hashtag[1].split('_')[0].split(':')[0]
        port = int(hashtag[1].split('_')[0].split(':')[1])
        s = None

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
                data = recvall(s)
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

            print(tup[0])
            answers = json.loads(tup[0])

            # Iterate through all answers and post status
            for item in answers:
                tweet1 = '@' + screen_name + ' Team_02 "' + item + '"'
                tweet2 = '@VTNetApps' + ' Team_02 "' + item + '"'

                tweet1 = (tweet1[:138] + '..') if (len(tweet1) > 140) else tweet1
                tweet2 = (tweet2[:138] + '..') if (len(tweet2) > 140) else tweet2

                # Tweet back to original sender
                api.update_status(tweet1)

                # Tweet to VTNetApps
                api.update_status(tweet2)
        except Exception as e:
            if s:
                s.close()
            print("ERROR: " + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def main():
    # Delete all tweets on timeline
    while True:
        delete = input("Delete all tweets? (Y/N): ").lower()
        if delete == 'y':
            batch_delete()
            print("All tweets deleted")
            break
        elif delete == 'n':
            break

    print("Now listening . . .")
    # Create a stream
    mystreamlistener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=mystreamlistener)

    # Start a stream - async makes the stream run on a new thread
    stream.userstream(async=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting client...")
        sys.exit(2)
