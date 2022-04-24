import requests
import json
import csv
import time

## import necessary packages
from datetime import datetime
from dateutil import rrule

year = 2020
queryStructure = "https://api.data.gov.sg/v1/transport/carpark-availability?date_time="
queryString = "https://api.data.gov.sg/v1/transport/carpark-availability?date_time=2022-03-08T09%3A00%3A00"

for mnth in range(1,13,1):
    endYear = year
    endMnth = mnth+1
    if endMnth >= 13:
        endMnth = 1
        endYear += 1
    start_date = datetime(year, mnth, 1, minute = 30)
    end_date = datetime(endYear, endMnth, 1, 0,0,0,0)
    carparkData = []

    # Handpicked 10 carparks
    carparkFilter = ["J69","J62M","J63","J67","J70","JM31","J72","J83M","JM2","J85M"]
    for dt in rrule.rrule(rrule.HOURLY, dtstart=start_date, until=end_date):
        print(dt)
        
        queryString = queryStructure + str(dt).replace(" ", "T").replace(":", "%3A")
        response = requests.get(queryString)
        failedTries = 0
        while response.status_code != 200:
            time.sleep(60) # Pause for a minute incase overload of request
            response = requests.get(queryString)
            failedTries += 1
            if failedTries >= 10:
                break
        
        if failedTries >= 10:
            time.sleep(600)
            continue
        responseDict = response.json()["items"]
        if (len(responseDict) == 0):
            continue
        dictLength = len(responseDict[0]["carpark_data"])
        i = 0
        while i < dictLength:
            if responseDict[0]["carpark_data"][i]['carpark_number'] in carparkFilter:
                responseDict[0]["carpark_data"][i].update({"timestamp": responseDict[0]["timestamp"]})
                responseDict[0]["carpark_data"][i].update({"total_lots": responseDict[0]["carpark_data"][i]["carpark_info"][0]["total_lots"]})
                responseDict[0]["carpark_data"][i].update({"lots_available": responseDict[0]["carpark_data"][i]["carpark_info"][0]["lots_available"]})
                responseDict[0]["carpark_data"][i].pop("carpark_info")
                i += 1
            else:
                # Filter out carparks
                responseDict[0]["carpark_data"].pop(i)
                dictLength = len(responseDict[0]["carpark_data"])
        responseDict[0].pop("timestamp", "Failed to remove timestamp")
        carparkData.extend(responseDict[0]["carpark_data"])
        time.sleep(2)

    with open('carpark_' + str(mnth) + '_' + str(year) + '.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=['carpark_number', 'update_datetime', 'timestamp', 'total_lots', 'lots_available'])
        dict_writer.writeheader()
        dict_writer.writerows(carparkData)
    
    time.sleep(60)
