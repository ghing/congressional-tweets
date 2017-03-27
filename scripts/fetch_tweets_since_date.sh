#!/bin/bash

set -eu

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -s|--since)
    SINCE="$2"
    shift # past argument
    ;;
    *)
    # unknown option
    ;;
esac
shift # past argument or value
done

while read screen_name 
do
  congressional_tweets fetch_tweets --since-date "$SINCE" "$screen_name" | congressional_tweets load_tweets
done < "${1:-/dev/stdin}"
