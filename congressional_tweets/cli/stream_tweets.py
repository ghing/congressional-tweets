import json
import os
import signal
import sys

import tweepy
import zmq


def handle_sigint(signum, frame):
    sys.exit()

signal.signal(signal.SIGINT, handle_sigint)


class StandardOutputStreamListener(tweepy.StreamListener):
    def set_socket(self, socket):
        self._socket = socket

    def on_status(self, status):
        self._socket.send_string('status ' + json.dumps(status._json))

    def on_error(self, status_code):
        print(status_code)
        # TODO: Better error handling
        # More on error codes here:
        # https://dev.twitter.com/overview/api/response-codes
        return False


def add_parser(subparsers):
    parser = subparsers.add_parser('stream_tweets',
        description="Stream Tweets for users via the Twitter API.")
    parser.add_argument('user_id', help="Screen name of the Twitter user.",
        nargs="+")

    parser.add_argument('--consumer-key',
        default=os.environ.get('TWITTER_CONSUMER_KEY'))
    parser.add_argument('--consumer-secret',
        default=os.environ.get('TWITTER_CONSUMER_SECRET'))
    parser.add_argument('--access-token',
        default=os.environ.get('TWITTER_ACCESS_TOKEN'))
    parser.add_argument('--access-token-secret',
        default=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))
    parser.add_argument('--url',
        default=os.environ.get('CONGRESSIONAL_TWEETS_STREAMING_URL',
            "tcp://127.0.0.1:5557"))

    parser.set_defaults(func=main)


def main(args):
    auth = tweepy.OAuthHandler(args.consumer_key, args.consumer_secret)
    auth.set_access_token(args.access_token, args.access_token_secret)
    api = tweepy.API(auth)

    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUB)
    zmq_socket.bind(args.url)

    # Docs on Tweepy streaming are here:
    # https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html

    stream_listener = StandardOutputStreamListener()
    stream_listener.set_socket(zmq_socket)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    # Use the filter streaming endpoint
    # Docs: https://dev.twitter.com/streaming/reference/post/statuses/filter
    #
    # Specify which users to follow
    # See docs at
    # https://dev.twitter.com/streaming/overview/request-parameters#follow
    stream.filter(follow=args.user_id)
