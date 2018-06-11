#!/bin/sh
#sed 's/is/IS/g': s is replace, is => IS, g is replace all data
#curl -s -XGET 'http://10.254.100.240:9200/_cat/indices?v' | grep logstash | awk '{print $3}' | sed 's/logstash-[0-9,.]*-//g' | sed 's/\./-/g'
#a=($(ls /home/data/elasticsearch/nodes/0/indices/ | sed 's/logstash-[0-9,.]*-//g' | sed 's/\./-/g'))

indexname=logstash-
day=8
tempday=$((24*60*60*$day))

array=($(curl -s -XGET 'http://172.16.1.56:9200/_cat/indices?v' | grep logstash | awk '{print $3}' | sed 's/logstash-//g' | sed 's/-[0-9,.]*//g' | sed 's/\./-/g'))

for ((i=0; i<${#array[@]}; i++))
do
  echo "index No."$i ",index day:" ${array[$i]}
  
  now=$(date "+%s")
  index_day_string=${array[$i]}
  #echo "now:"$now
  
  indexday=$(date -d "${array[$i]}" +"%s")  
  #echo $indexday
  distanceofday=$((now-indexday))
  echo "difference:"$distanceofday
  echo "tempday:"$tempday
  if test "$distanceofday" -gt "$tempday"
  then
    #echo "exceed"
    escmd="curl -XDELETE http://172.16.1.56:9200/"$indexname$(echo $index_day_string | sed -e 's/-/./g')"*"
    echo $escmd 
    $escmd
  else
    echo "not exceed"
  fi  
  printf '\n'
done

#date -d "${array[2]}" +"%s"
