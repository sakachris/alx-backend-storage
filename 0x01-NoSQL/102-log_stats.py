#!/usr/bin/env python3
''' 102-log_stats.py '''

from pymongo import MongoClient
from collections import Counter


def log_stats(mongo_collection):
    '''
    provides some stats about Nginx logs stored in MongoDB
    '''
    total_logs = mongo_collection.count_documents({})

    print("{} logs".format(total_logs))

    print('Methods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"}
    )
    print("{} status check".format(status_check_count))

    ips = Counter(doc['ip'] for doc in mongo_collection.find())
    top_ips = ips.most_common(10)

    print("IPs:")
    for ip, count in top_ips:
        print("\t{}: {}".format(ip, count))


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = client.logs.nginx

    log_stats(log_collection)
