#!/bin/bash

set -eu

while read screen_name 
do
  last_id=$(congressional_tweets last_id "$screen_name" || echo "")
  if [ -n "$last_id" ]; then
    congressional_tweets fetch_tweets --since-id="$last_id" "$screen_name" | congressional_tweets load_tweets
  fi
done < "${1:-/dev/stdin}"
