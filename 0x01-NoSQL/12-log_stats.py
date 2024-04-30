#!/usr/bin/env python3
""" module with one function update_topics"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    ops = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for op in ops:
        nb_op = nginx_collection.count_documents({"method": op})
        print(f"\tmethod {op}: {nb_op}")
    filter = {"method": "GET", "path": "/status"}
    cpt_filter = nginx_collection.count_documents(filter)
    print(f"{cpt_filter} status check")
