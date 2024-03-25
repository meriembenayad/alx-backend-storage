#!/usr/bin/env python3
""" 8. List all documents in Python """


def list_all(mongo_collection):
    """ Display all documents in a collection """
    return list(mongo_collection.find())
