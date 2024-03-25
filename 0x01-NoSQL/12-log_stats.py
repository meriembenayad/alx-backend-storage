#!/usr/bin/env python3
""" 12. Log stats """
from pymongo import MongoClient

# Establish a connection to mongoDB server
client = MongoClient('mongodb://127.0.0.1:27017')

# Select a database 'logs'
db = client['logs']

# Select a collection 'nginx'
col = db['nginx']

# count documents in the collection
num_docs = db.col.count_documents({})
print(f'{num_docs} logs')

# List the methods
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

print('Methods:')
# Print the counts for each method
for method in methods:
    count = col.count_documents({'method': method})
    print(f'\tMethod {method}: {count}')

# Check the number ofdocuments with the method=GET and path=/status
check_status = col.count_documents({'method': 'GET', 'path': '/status'})
print(f'{check_status} status check')
