import requests
import json
import csv
import time

## import necessary packages
from datetime import datetime
from dateutil import rrule

# start_date = datetime(2021, 11, 1, minute = 30)
# start_date = datetime(2021, 11, 28, 0,30,0,0)
# end_date = datetime(2021, 11, 28, 2,0,0,0)
 
# start_date = datetime(2019, 1, 1, minute = 30)
# end_date = datetime(2021, 1, 20, 0,0,0)
# Start, (Ending Month), 6,12 = month 6 - 12
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
    # 159 Carparks in Punngol Area
    # carparkFilter = ["HG3B", "HG3D", "HG3E", "HG3L", "P1", "P2", "P3", "P34L", "P35L", "P4", "P5", "P5L", "P6", 
    # "P6L", "P7", "P73L", "P8", "P9", "PDS1", "PL10", "PL11", "PL12", "PL13", "PL14", "PL15", "PL16", "PL19", 
    # "PL23", "PL24", "PL25", "PL27", "PL28", "PL29", "PL30", "PL31", "PL32", "PL33", "PL34", "PL35", "PL36", 
    # "PL37", "PL38", "PL39", "PL40", "PL41", "PL42", "PL43", "PL44", "PL46", "PL47", "PL48", "PL49", "PL50", 
    # "PL51", "PL52", "PL53", "PL54", "PL55", "PL56", "PL59", "PL60", "PL61", "PL62", "PL65", "PL66", "PL67", 
    # "PL68", "PL70", "PL75", "PL78", "S100", "S102", "S103", "S104", "S105", "S107", "S108", "S109", "S110", 
    # "S113", "S13L", "S14L", "S30L", "SK1", "SK10", "SK11", "SK12", "SK13", "SK14", "SK15", "SK16", "SK17", 
    # "SK18", "SK19", "SK2", "SK20", "SK21", "SK22", "SK23", "SK24", "SK25", "SK26", "SK27", "SK28", "SK29", 
    # "SK3", "SK30", "SK31", "SK32", "SK33", "SK34", "SK35", "SK36", "SK37", "SK38", "SK39", "SK40", "SK41", 
    # "SK42", "SK43", "SK44", "SK45", "SK46", "SK47", "SK48", "SK49", "SK5", "SK50", "SK51", "SK52", "SK53", 
    # "SK55", "SK59", "SK6", "SK63", "SK64", "SK65", "SK66", "SK68", "SK7", "SK70", "SK72", "SK73", "SK76", 
    # "SK79", "SK8", "SK82", "SK84", "SK89", "SK9", "SK90", "SK91", "SK92", "SK94", "SK95", "SK96", "SK97", "SK98", "SK99"]

    # Handpicked 10 carparks
    # carparkFilter = ["S14L","S113","S110","SK97","SK53","SK46","SK47","SK44","SK40","SK41"]
    carparkFilter = ["J69","J62M","J63","J67","J70","JM31","J72","J83M","JM2","J85M"]
    # 2 of them have very carpark amount - unsually full. 
    # carparkFilter = ["S14L","S13L","S110","SK97","SK53","SK46","SK47","SK44","SK49","SK41", "SK36","SK42","SK37"]
    for dt in rrule.rrule(rrule.HOURLY, dtstart=start_date, until=end_date):
        print(dt)
        
        queryString = queryStructure + str(dt).replace(" ", "T").replace(":", "%3A")
        response = requests.get(queryString)
        failedTries = 0
        while response.status_code != 200:
            time.sleep(30) # Pause for a minute incase overload of request
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
                # responseDict[0]["carpark_data"][i].update({"lot_type": responseDict[0]["carpark_data"][i]["carpark_info"][0]["lot_type"]})
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
    # keys = carparkData[0].keys()
    # print(keys)

    with open('carpark_' + str(mnth) + '_' + str(year) + '.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=['carpark_number', 'update_datetime', 'timestamp', 'total_lots', 'lots_available'])
        dict_writer.writeheader()
        dict_writer.writerows(carparkData)
    
    time.sleep(60)