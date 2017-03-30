import json
import os
from urllib.parse import urlparse

from pymongo import MongoClient
import zmq


def add_parser(subparsers):
    parser = subparsers.add_parser('load_streamed_tweets',
        description="Load Tweets into a MongoDB database.")

    parser.add_argument('--database', help="URL for MongoDB database.",
        default=os.environ.get('CONGRESSIONAL_TWEETS_DB_URL',
            "mongodb://localhost:27017/congressional-tweets"))
    parser.add_argument('--collection', help="MongoDB collection",
        default="tweets")
    parser.add_argument('--url',
        default=os.environ.get('CONGRESSIONAL_TWEETS_STREAMING_URL',
            "tcp://127.0.0.1:5557"))

    parser.set_defaults(func=main)


def parse_msg(msg):
    json_start = msg.find('{')
    topic = msg[:json_start].strip()
    data = msg[json_start:]
    return topic, data


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

    context = zmq.Context()
    receiver = context.socket(zmq.SUB)
    receiver.connect(args.url)
    receiver.setsockopt_string(zmq.SUBSCRIBE, 'status')

    while True:
        topic, status = parse_msg(receiver.recv_string())
        status_data = json.loads(status)
        collection.insert_one(status_data)
