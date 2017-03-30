import os

import zmq


def add_parser(subparsers):
    parser = subparsers.add_parser('display_streamed_tweets',
        description="Display streamed tweets.")

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
    context = zmq.Context()
    receiver = context.socket(zmq.SUB)
    receiver.connect(args.url)
    receiver.setsockopt_string(zmq.SUBSCRIBE, 'status')

    while True:
        topic, status = parse_msg(receiver.recv_string())
        print(status)
