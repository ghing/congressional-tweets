congressional-tweets
====================

Fetch and store Tweets for members of congress.  Really this will work for any users tweets, but I'm using it for tweets by members of the United States House of Representatives.

Fetch tweets
------------

    congressional_tweets fetch_tweets --since-date 2017-01-20 RepMarthaRoby

Load tweets
-----------

    congressional_tweets fetch_tweets --since-date 2017-01-20 RepMarthaRoby | \
    congressional_tweets load_tweets

Load only unsaved tweets
------------------------

    congressional_tweets fetch_tweets --since-id=`congressional_tweets last_id RepMarthaRoby` RepMarthaRoby | \
    congressional_tweets load_tweets

Load tweets for a number of representatives since a given date
--------------------------------------------------------------

    ./scripts/fetch_tweets_since_date.sh --since 2017-01-19 RepJohnDelaney RepMGriffith RepHalRogers repgoodlatte DrPhilRoe

Load unseen tweets
------------------

That command is good for doing an initial load of tweets from representatives.  However, the API calls are more efficient if you load tweets since a previously-seen tweet ID rather than a date.  To do that, you could run this script:

    ./scripts/fetch_unseen_tweets.sh RepJohnDelaney RepMGriffith RepHalRogers repgoodlatte DrPhilRoe

Search for tweets
-----------------

    congressional_tweets search_tweets ".*Town Hall.*" ".*townhall.*" |\
    ndjson-map '{"screen_name": d.user.screen_name, "text": d.text, "id": d.id_str, "created_at": d.created_at, "url": "https://twitter.com/" + d.user.screen_name + "/status/" + d.id_str}' |\
    in2csv --format ndjson > tweets.csv

This example uses the super-helpful [ndjson-cli](https://github.com/mbostock/ndjson-cli) program to filter out only the most useful fields for human review from the database.

It also uses the `in2csv` command from csvkit to convert from ndjson to CSV to more easily view records in tabular format.some of the tweets from the database.

Stream tweets into a database
-----------------------------

    congressional_tweets load_stream_tweets
    congressional_tweets stream_tweets

Running on systemd
------------------

In production, I'm using systemd on Ubuntu 16.04 to supervise the `load_stream_tweets` and `stream_tweets` commands.  You can find some example unit files for runnig these commands as systemd services in the `systemd` directory.
