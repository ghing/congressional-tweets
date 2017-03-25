import argparse
import json
import sys
from urllib.parse import urlparse

from pymongo import MongoClient


def add_parser(subparsers):
    parser = subparsers.add_parser('load_tweets',
        description="Load Tweets into a MongoDB database.")

    parser.add_argument('--database', help="URL for MongoDB database.",
        default="mongodb://localhost:27017/congressional-tweets")
    parser.add_argument('--collection', help="MongoDB collection",
        default="tweets")
    parser.add_argument('--input', type=argparse.FileType('r'),
        default=sys.stdin)

    parser.set_defaults(func=main)

def main(args):
    parsed = urlparse(args.database)
    db_url = "{scheme}://{hostname}:{port}".format(
        scheme=parsed.scheme,
        hostname=parsed.hostname,
        port=parsed.port)
    database = parsed.path.lstrip('/').split('/')[0]
            
    client = MongoClient(db_url)
    db = client[database]

    collection = db[args.collection]

    for line in args.input:
        status = json.loads(line)
        collection.insert_one(status)
