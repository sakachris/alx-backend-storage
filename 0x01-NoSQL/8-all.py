#!/usr/bin/env python3
''' 8-all.py '''


def list_all(mongo_collection):
    '''
    lists all documents in a collection
    '''
    docs = [doc for doc in mongo_collection.find()]

    return docs
