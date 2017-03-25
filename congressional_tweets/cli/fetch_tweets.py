from datetime import datetime, timedelta
import json
import os

import tweepy

def add_parser(subparsers):
    parser = subparsers.add_parser('fetch_tweets',
        description="Fetch Tweets for a user via the Twitter API.")
    parser.add_argument('screen_name', help="ID of the Twitter user.")

    parser.add_argument('--since-date', help="Return only tweets since this date.")
    parser.add_argument('--since-id', help="Return only tweets after this ID.")
    parser.add_argument('--count', help="Number of tweets to return per-page",
        default=100)
    parser.add_argument('--consumer-key',
        default=os.environ.get('TWITTER_CONSUMER_KEY'))
    parser.add_argument('--consumer-secret',
        default=os.environ.get('TWITTER_CONSUMER_SECRET'))
    parser.add_argument('--access-token',
        default=os.environ.get('TWITTER_ACCESS_TOKEN'))
    parser.add_argument('--access-token-secret',
        default=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

    parser.set_defaults(func=main)

def main(args):
    auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
    auth.set_access_token(args.access_token, args.access_token_secret)

    since_date = None
    since_id = None

    if args.since_date is not None:
        since_date = datetime.strptime(args.since_date, '%Y-%m-%d').date()
    elif args.since_id is not None:
        since_id = args.since_id
    else:
        since_date = (datetime.now() - timedelta(days=365)).date()

    api = tweepy.API(auth)

    # QUESTION: should this start at 0 or 1
    page = 0

    while page is not None:
        kwargs = {
            'id': args.screen_name,
            'screen_name': args.screen_name,
            'count': args.count,
            'page': page
        }

        if since_id is not None:
            kwargs['since_id'] = since_id

        statuses = api.user_timeline(**kwargs)
        if len(statuses) == 0:
            break

        for status in statuses:
            if since_date is not None and status.created_at.date() <= since_date:
                page = None
                break

            print(json.dumps(status._json))

        if page is not None:
            page += 1
