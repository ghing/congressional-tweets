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

Assuming you have a file with one screen name per row:

    cat appalachian_reps_twitter_screen_names.txt | ./scripts/fetch_tweets_since_date.sh --since 2017-01-19

Load unseen tweets
------------------

That command is good for doing an initial load of tweets from representatives.  However, the API calls are more efficient if you load tweets since a previously-seen tweet ID rather than a date.  To do that, you could run this script:

    cat appalachian_reps_twitter_screen_names.txt | ./scripts/fetch_unseen_tweets.sh

Search for tweets
-----------------

    congressional_tweets search_tweets ".*Town Hall.*" ".*townhall.*" | ndjson-map '{"screen_name": d.user.screen_name, "text": d.text, "id": d.id, "created_at": d.created_at}'

This example uses the super-helpful [ndjson-cli](https://github.com/mbostock/ndjson-cli) program to filter out some of the tweets from the database.
