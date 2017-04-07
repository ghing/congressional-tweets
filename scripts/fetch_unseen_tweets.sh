#!/bin/bash

set -eu

for screen_name in "$@"
do
  last_id=$(congressional_tweets last_id --screen-name="$screen_name" || echo "")
  if [ -n "$last_id" ]; then
    congressional_tweets fetch_tweets --since-id="$last_id" "$screen_name" | congressional_tweets load_tweets
  fi
done
