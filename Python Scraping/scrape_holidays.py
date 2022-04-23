import requests
import json
import csv



for year in range (2016,2022):
    url = 'https://rjchow.github.io/singapore_public_holidays/api/' + str(year) + '/data.json'
    response = requests.get(url=url)
    data = response.json()

    with open('sg_holidays.csv', 'a+', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=['Date', 'Day', 'Name', 'Observance', 'Observance Strategy'])
            if year == 2016:
                dict_writer.writeheader()
            dict_writer.writerows(data)