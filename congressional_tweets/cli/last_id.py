import re
import sys
from urllib.parse import urlparse

from pymongo import MongoClient, DESCENDING


def add_parser(subparsers):
    parser = subparsers.add_parser('last_id',
        description="Get the last saved tweet ID for a given screen name or query.")

    parser.add_argument('--screen-name', help="ID of the Twitter user.")
    parser.add_argument('--query', help="Regex to search for in tweet text.",
        nargs='*')

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

    find_args = {}

    if (args.screen_name is not None and args.query is not None and
            len(args.query)):
        find_args['$and'] = [
            {
                'user.screen_name': args.screen_name,
            },
        ]
        text_query = []
        find_args['$and'].append({
            '$or': text_query,
        })

        for query in args.query:
            text_query.append({
                'text': {
                    '$regex': re.compile(query, re.IGNORECASE),
                },
            })

    elif args.screen_name is not None:
        find_args['user.screen_name'] = args.screen_name

    elif args.query is not None and len(args.query):
        find_args['$or'] = []

        for query in args.query:
            find_args['$or'].append({
                'text': {
                    '$regex': re.compile(query, re.IGNORECASE),
                },
            })

    else:
        sys.stderr.write("You must specify either the a screen name, query or both.\n")
        sys.exit(1)

    try:
        status = collection.find(find_args).sort('id', DESCENDING)[0]
        print(status['id'])
    except IndexError:
        sys.stderr.write("No tweets found\n")
        sys.exit(1)
