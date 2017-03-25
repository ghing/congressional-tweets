import sys
from urllib.parse import urlparse

from pymongo import MongoClient, DESCENDING

def add_parser(subparsers):
    parser = subparsers.add_parser('last_id',
        description="Get the last saved tweet ID for a given screen name")

    parser.add_argument('screen_name', help="ID of the Twitter user.")

    parser.add_argument('--database', help="URL for MongoDB database.",
        default="mongodb://localhost:27017/congressional-tweets")
    parser.add_argument('--collection', help="MongoDB collection",
        default="tweets")

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

    try:
        status = collection.find({
            'user.screen_name': args.screen_name,
        }).sort('id', DESCENDING)[0]
        print(status['id'])
    except IndexError:
        sys.stderr.write("No tweet found for screen name {}\n".format(args.screen_name))
        sys.exit(1)

