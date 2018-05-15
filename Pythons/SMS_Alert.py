#!/usr/bin/python
# Aim:
#   1. Check if unusual event occurred.
#   2. If so, send a POST request to SMS Alert Server;
import requests
import json
import os
from time import strftime
from elasticsearch import Elasticsearch


def event_logger(log, severity="INFO", dirpath="/var/log/python-elasticsearch/"):
    logpath = "Alert_Recorder_{}.log".format(strftime("%Y-%m-%d"))
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(logpath, "a") as f:
        f.write(strftime('[%Y-%m-%dT%H:%M:%S][') + str(severity) + "] " + str(log)+"\n")
    # Log events to syslog.


def getReceivers():
    # No alert level yet.
    return [
        "0912345678",
        "0987654321"
    ]
    # Whom will be Notified.


def getAggResult(esHost, esPort, esIndex, term1, agg1):
    queryBody = {
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "@timestamp": {
                            "gte": "now-1d"
                        }
                    }
                }
            }
        },
        "aggs": {
            "TERM1": {
                "terms": {
                    "field": term1,
                    "size": 2000
                },
                "aggs": {
                    "AGG1": {
                        "terms": {
                            "field": agg1,
                            "size": 1
                        }
                    }
                }
            }
        }
    }
    es = Elasticsearch(host=esHost, port=esPort)
    output = es.search(index=esIndex, body=queryBody)
    return output


def POST_Sender(PhoneNumber, IndexName, LoginID, QueryField, Threshold):
    target_URL = "http://123.45.67.89/smsAPI/Sms/SendSMS"
    headers = {
        "Content-Length": "149",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
        "Host": "123.45.67.89"
    }
    payload = {
        "BUSINESSCODE": "AAJQ6V",
        "IDENTIFIER": "X08v59LPg7m79ZNda5PDHP7KqnFcjd",
        "DA": str(PhoneNumber),
        "STOPTIME": "",
        "CUSID": "",
        "TEMPLATEVAR": {
            "IndexName": IndexName,
            "LoginID": LoginID,
            "QueryField": QueryField,
            "Threshold": Threshold,
        }
    }
    r = requests.post(target_URL, headers=headers, data=payload)
    return json.load(r.text)
    # POST to SMS Server


def main():
    # Part 0: Get ES check Commands and Receivers.
    es_host = "127.0.0.1"
    es_port = "9200"
    IndexDict = {
        "cims_log-{}".format(strftime('%Y.%m.%d')): {
            "TERM1": "LoginID",
            "AGG1": "CustomerID",
            "Threshold": 1
        }
    }
    Receivers = getReceivers()

    # Part 1: Check Events
    for SysIndex in IndexDict.keys():
        res = getAggResult(es_host, es_port, SysIndex, IndexDict[SysIndex]["TERM1"], IndexDict[SysIndex]["AGG1"])
        if int(res["hits"]["total"]) == 0:
            event_logger("{}: got 0 hits".format(SysIndex), severity="WARN")
        else:
            for bks in res["aggregations"]["TERM1"]["buckets"]:
                if len(bks["AGG1"]["buckets"]) == 0:
                    pass
                elif bks["AGG1"]["buckets"][0]["doc_count"] > int(IndexDict[SysIndex]["Threshold"]):
                    UnusualID = bks["key"]
                    QueriedField = IndexDict[SysIndex]["AGG1"]
                    Threshold = IndexDict[SysIndex]["Threshold"]
                    event_logger("Unusual Event! LoginID: [{0}] is exceeded the threshold[{1}]".format(UnusualID, Threshold), "WARN")

                    # Part 2: POST requests to SMS Server to Send Alerts.
                    RowId_List = []
                    ErrorCode_List = []
                    for r in Receivers:
                        res = POST_Sender(r, SysIndex, UnusualID, QueriedField, Threshold)
                        RowId_List.append(res[0])
                        ErrorCode_List.append(res[1])


if __name__ == "__main__":
    main()
