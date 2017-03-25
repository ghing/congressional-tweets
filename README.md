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
