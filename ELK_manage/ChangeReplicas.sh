#!/bin/sh

# You cat put index list in indexList.txt
# By curl -XGET "ES_ip:ES_port/_cat/indices" |awk '{}'
post="{"index" : {"number_of_replicas" : 0}}"

cat indexList.txt | \
while read CMD; do
    echo curl -XPUT "ES_ip:ES:port/$CMD/_settings" -d "${post}"
done


# OR, curl -XPUT "ES_ip:ES:port/_all/_settings" -d "${post}"
