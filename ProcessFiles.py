import gzip
import shutil
import json
import pprint
import os
import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import collections

def loop_through_file(directory):
    #Get the full path for rach file in the directory and pass the path to unzip_file function
    for subdir, dirs, files in os.walk(directory):
        count = 0
        for filename in files:
            unzip_file(subdir + os.sep + filename,count)
            count += 1


def unzip_file(filename,index):
    #Unzip the file received as parameter and creates a txt file named txt + the index received as parameter
    with gzip.open(filename) as f_in:
        with open(f"C:\\Users\\niuonas\\Documents\\PythonCode\\ReadJSONFiles\\JsonFile\\txt{index}.txt","wb") as f_out:
            shutil.copyfileobj(f_in,f_out)


def read_json(filename):
    print("test")


def json_to_csv(filename):
    json_file = pd.read_json(r"C:\Users\niuonas\Desktop\RWAC DNAlog files\aea3d2d142.2020-05-18.76.ld76.json", lines=True)
    json_file.to_csv("test.csv")




if __name__ == "__main__":
    #Unzip every file from the archive
    loop_through_file(r"C:\Users\niuonas\Desktop\RWAC DNAlog files")

    #Combine the content from every Json file into a single list of dicts
    json_data = []
    for subdir, dirs, files in os.walk(r"C:\Users\niuonas\Documents\PythonCode\ReadJSONFiles\JsonFile"):
        for filename in files:
            json_file = subdir + os.sep + filename
            
            try:
                json_content = open(json_file)
            except UnicodeDecodeError:
                print(filename + "cant be read!")

            for line in json_content:
                json_line = json.loads(line)
                json_data.append(json_line)
    
    #Set indentation for pretty print
    pp = pprint.PrettyPrinter(indent=4)

    #Loop thorugh every element in the Json list and get the information
    versionList = []
    versionListComplete = []
    totalEntries = 0
    entriesWithBadVersion = 0
    ipList = []
    timeZones = []
    productionYearSerialNumberDict = {}
    listOfOddSerialNumbers = []

    SerialNumberYear = {
        "A" : "2001", 
        "B" : "2002", 
        "C" : "2003",
        "D" : "2004", 
        "E" : "2005", 
        "F" : "2006", 
        "G" : "2007", 
        "H" : "2008",  
        "J" : "2009", 
        "K" : "2010",
        "M" : "2011",
        "N" : "2012",
        "P" : "2013",
        "Q" : "2014",
        "R" : "2015",
        "S" : "2016",
        "T" : "2017",
        "U" : "2018",
        "V" : "2019",
        "W" : "2020",
        "X" : "2021",
        "Y" : "2022",
        "Z" : "2023",
        "2" : "2024",
        "3" : "2025",
        "4" : "2026",
        "5" : "2027",
        "6" : "2028",
        "7" : "2029",
        "8" : "2030"
    }

    for index in range(len(json_data)):
        #Total number of line
        totalEntries += 1

        #Add to version number list each element
        versionListComplete.append(json_data[index]["_source"]["_meta"]["Version"])

        #Add each timezone to timezone list
        timeZones.append(json_data[index]["_source"]["_meta"]["Timezone"])

        #Check if the admin console ip is unique or not
        if(json_data[index]["_source"]["_ip"] not in ipList):
            ipList.append(json_data[index]["_source"]["_ip"])
        
        #Check if the serial number is unset
        if json_data[index]["_source"]["_meta"]["SerialNumber"] == "ABC123":
            versionList.append(json_data[index]["_source"]["_meta"]["Version"])
            entriesWithBadVersion += 1
        elif(len(json_data[index]["_source"]["_meta"]["SerialNumber"].strip()) == 11):
            productionYearSerialNumberDict[json_data[index]["_source"]["_meta"]["SerialNumber"]] = [SerialNumberYear[json_data[index]["_source"]["_meta"]["SerialNumber"][4]]]
        else:
            listOfOddSerialNumbers.append(json_data[index]["_source"]["_meta"]["SerialNumber"])
    
    #Count how many time zones there are
    timeZones_dict = Counter(timeZones)

    #Count how many versions are
    version_occurance_rate_complete = Counter(versionListComplete)

    #Count how many unset serial numbers per version and save the information in a dictionary
    version_occurance_rate = Counter(versionList)

    #Sort the time zones dictionary by values
    sorted_list = sorted(timeZones_dict.items(), key = lambda x:x[1], reverse=True)
    timeZones_dict = collections.OrderedDict(sorted_list)

    #Sort the unset versions dictionary by key values
    sorted_list = sorted(version_occurance_rate.items(), key = lambda x:x[1], reverse=True)
    version_occurance_rate = collections.OrderedDict(sorted_list)

    #Sort the all versions dictionary by key values
    sorted_list = sorted(version_occurance_rate_complete.items(), key = lambda x:x[1], reverse=True)
    version_occurance_rate_complete = collections.OrderedDict(sorted_list)

    #Print the dict to have as reference
    pp.pprint(productionYearSerialNumberDict)
    pp.pprint(listOfOddSerialNumbers)

    #Bar chart that showcase total number of versions
    plt.bar(version_occurance_rate_complete.keys(), version_occurance_rate_complete.values(), width = 0.8, color = "b", align = 'center')
    plt.xticks(rotation=90)
    plt.locator_params(axis="y", nbins=20)
    plt.show()

    #Bar chart that showcase total number of time zones
    plt.bar(timeZones_dict.keys(), timeZones_dict.values(), width = 0.8, color = "b", align = 'center')
    plt.xticks(rotation=90)
    plt.locator_params(axis="y", nbins=20)
    plt.show()

    #Bar chart showing the amount of unset serial numbers per version
    plt.bar(version_occurance_rate.keys(), version_occurance_rate.values(), width = 0.8, color = "r", align = 'center')
    plt.xticks(rotation=90)
    plt.locator_params(axis="y", nbins=20)
    plt.show()

    #Pie chart that showcase bad version vs correct versions
    labels = f'Unset Serial Numbers ({entriesWithBadVersion})', f'Set Serial Numbers ({totalEntries - entriesWithBadVersion})'
    sizes = [entriesWithBadVersion, totalEntries - entriesWithBadVersion]
    colors = ['red','green']
    explode = (0.1, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode = explode, labels = labels, autopct='%1.1f%%', shadow=True, startangle=90, colors = colors)
    ax1.axis('equal')

    plt.show()