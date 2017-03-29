import os
import sys

import tweepy


def add_parser(subparsers):
    parser = subparsers.add_parser('screen_name_to_id',
        description="Convert Twitter screen name to ID")

    parser.add_argument('--sep',
        help="Separate IDs with this string", default=" ")
    parser.add_argument('--consumer-key',
        default=os.environ.get('TWITTER_CONSUMER_KEY'))
    parser.add_argument('--consumer-secret',
        default=os.environ.get('TWITTER_CONSUMER_SECRET'))
    parser.add_argument('--access-token',
        default=os.environ.get('TWITTER_ACCESS_TOKEN'))
    parser.add_argument('--access-token-secret',
        default=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

    parser.add_argument('screen_name',
        help="Regex to search for in tweet text.", nargs='+')

    parser.set_defaults(func=main)


def get_id(screen_name, api):
    user = api.get_user(screen_name=screen_name)
    return user.id_str


def main(args):
    auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
    auth.set_access_token(args.access_token, args.access_token_secret)
    api = tweepy.API(auth)

    ids = [get_id(sn, api) for sn in args.screen_name]
    sys.stdout.write(args.sep.join(ids))
