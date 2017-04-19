import re
from urllib.parse import urlparse

from pymongo import MongoClient, DESCENDING
from bson.json_util import dumps


def add_parser(subparsers):
    parser = subparsers.add_parser('search_tweets',
        description="Search for tweets in a MongoDB database.")

    parser.add_argument('--database', help="URL for MongoDB database.",
        default="mongodb://localhost:27017/congressional-tweets")
    parser.add_argument('--collection', help="MongoDB collection",
        default="tweets")
    parser.add_argument('--screen-name',
        help="Only search tweets from this screen name.",
        action='append')
    parser.add_argument('--since-id',
        help="Only search tweets with IDs greater than this ID.")

    parser.add_argument('query', help="Regex to search for in tweet text.",
        nargs='+')

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

    if args.screen_name is not None or args.since_id is not None:
        find_args['$and'] = []
        if args.screen_name is not None:
            find_args['$and'].append(
                {
                    'user.screen_name': {
                        '$in': args.screen_name,
                    },
                },
            )

        if args.since_id is not None:
            find_args['$and'].append(
                {
                    'id': {
                        '$gt': int(args.since_id),
                    },
                },
            )

        text_query = []
        find_args['$and'].append({
            '$or': text_query,
        })

    else:
        find_args['$or'] = []
        text_query = find_args['$or']

    for query in args.query:
        text_query.append({
            'text': {
                '$regex': re.compile(query, re.IGNORECASE),
            },
        })

    for tweet in collection.find(find_args).sort('id', DESCENDING):
        print(dumps(tweet))
