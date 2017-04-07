#!/bin/bash

set -eu

screen_names=""

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
    screen_names="$screen_names $key"
    ;;
esac
shift # past argument or value
done

screen_names="$screen_names $1"

for screen_name in $screen_names
do
  congressional_tweets fetch_tweets --since-date "$SINCE" "$screen_name" | congressional_tweets load_tweets
done
