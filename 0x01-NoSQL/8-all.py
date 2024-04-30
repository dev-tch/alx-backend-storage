#!/usr/bin/env python3
""" module with one function list_all"""
import pymongo


def list_all(mongo_collection):
    """ function that lists all documents in a collection"""
    return mongo_collection.find()
