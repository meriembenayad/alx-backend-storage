#!/usr/bin/env python3
""" 15. Log stats - New version """
from pymongo import MongoClient

if __name__ == "__main__":
    # Establish a connection to mongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')
    # Select a database 'logs'
    db = client['logs']
    # Select a collection 'nginx'
    col = db['nginx']
    # count documents in the collection
    num_docs = col.count_documents({})
    print(f'{num_docs} logs')
    # List the methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    # Print the counts for each method
    for method in methods:
        count = col.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')
    # Check the number ofdocuments with the method=GET and path=/status
    check_status = col.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{check_status} status check')

    print('IPs:')
    ips_list = {}
    # Use MongoDB's aggregation framework to get the top 10 IPs
    top_ips = col.aggregate([
        {
            '$group': {
                '_id': '$ip',
                'count': {'$sum': 1}
            }
        },
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])

    # Prints the total:
    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')
