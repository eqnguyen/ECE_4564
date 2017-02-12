# ECE_4564

This project uses api's to automatically respont to tweets with questions. 

The format for a question in a tweet is as follows

@NetAppBoyz #172.30.33.25:50000_"What is a hokie?"
	Where the following
	172.30.33.25 - the local ip address where the server is running
	50000 - the port the server is listening for connections on
	What is a hokie? - the question being asked


Client initialization procedures:
Prompt user to delete all tweets, to keep account clean. 
Begin stream listener for reading tweets

Server initialization procedures: 
Setup server to allow tcp connections
Begin listening for those connections

Extra libraries:
hashlib - used for computing md5 hashes
