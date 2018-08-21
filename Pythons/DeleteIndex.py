import sys
from elasticsearch import Elasticsearch
import datetime


# calculate days from input date to now.
def days_from_now(input_date):
    if "." not in input_date:
        sys.exit("Something wrong in the Date format.")
    else:
        # transfer date string to datetime.date object.
        array = input_date.split(".")
        if len(array) != 3:
            sys.exit("Something wrong in the Date format.")
        d1 = datetime.date(int(array[0]), int(array[1]), int(array[2]))

        # transfer today date to datetime.date object
        d_now = datetime.datetime.now().strftime("%Y.%m.%d").split(".")
        d0 = datetime.date(int(d_now[0]), int(d_now[1]), int(d_now[2]))

        # count days difference
        delta = d0 - d1
        return delta.days  # return in integer.


# Read keeping days.
def fetch_yaml_to_dict():
    keep_dict = {}
    with open(".\\log_yaml", "r") as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line.startswith("#"):
                li = stripped_line.split(":")
                key = li[0]
                value = li[1].strip()
                try:
                    keep_dict[key] = int(value)
                except TypeError:
                    sys.exit("Something is WRONG in the yaml file.")
    return keep_dict


def main():
    # Get days dict.
    days_dict = fetch_yaml_to_dict()

    # Create Elasticsearch object to control.
    es = Elasticsearch(hosts="127.0.0.1:1859", http_auth=("logstash", "logstash"))
    indices = es.indices.get("*").keys()  # Fetch all indices.
    
    # Traversal all indices and check if expired.
    while len(indices) > 0:
        i = indices.pop(0)
        index_name = i[0:-11]  # Get index name.
        index_date = i[-10:]   # Get index date.
        if days_from_now(index_date) > days_dict[index_name]:  # Check if index_date exceed keeping days.
            es.indices.delete(index=i, ignore=[400, 404])      # If so, delete it.
