import argparse

from congressional_tweets.cli.fetch_tweets import add_parser as fetch_tweets_add_parser
from congressional_tweets.cli.load_tweets import add_parser as load_tweets_add_parser
from congressional_tweets.cli.last_id import add_parser as last_id_add_parser
from congressional_tweets.cli.search_tweets import add_parser as search_tweets_add_parser
from congressional_tweets.cli.stream_tweets import add_parser as stream_tweets_add_parser
from congressional_tweets.cli.screen_name_to_id import add_parser as screen_name_to_id_add_parser
from congressional_tweets.cli.display_tweets import add_parser as display_streamed_tweets_add_parser


def main():
    parser = argparse.ArgumentParser(prog='congresssional_tweets')
    subparsers = parser.add_subparsers(help="sub-command help")

    fetch_tweets_add_parser(subparsers)
    load_tweets_add_parser(subparsers)
    last_id_add_parser(subparsers)
    search_tweets_add_parser(subparsers)
    stream_tweets_add_parser(subparsers)
    screen_name_to_id_add_parser(subparsers)
    display_streamed_tweets_add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)
