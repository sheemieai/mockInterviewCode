import datetime
import time
from collections import defaultdict

entries = [ "2021-01-01 00:00:00, 00002, Online",
            "2021-01-01 00:30:00, 00001, Offline",
            "2021-01-01 05:00:00, 00001, In Use",
            "2021-01-01 06:00:00, 00002, Offline",
            "2021-01-02 06:30:00, 00001, In Use",
            "2021-01-02 07:30:00, 00001, In Use",
            "2021-01-01 07:45:00, 00001, In Use",
            "2021-01-01 07:45:01, 00001, In Use",
            "2021-01-01 07:45:30, 00002, Offline",
            "2021-01-01 07:45:45, 00003, Offline"]


def convertTimeToSeconds(timeToFormat):
    x = time.strptime(timeToFormat.split(',')[0],'%H:%M:%S')
    result = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()   
    return result


# seperates data by device number, dictionary {device_number:[data]} format
def seperateDataByDevice(arrayToSeperate):
    seperated_data = seperateEntriesData(arrayToSeperate)
    device_dic = defaultdict(list)

    for entry in seperated_data:
        device_dic[entry[1]].append(entry)
    return device_dic


# list of the entries' lines seperated into [time, device number, date, avaibility] format
def seperateEntriesData(arrayToFormat):
    formatted_data = []
    #seperated data into a list
    seperated_data = [line.split() for line in arrayToFormat]

    # fix the data list
    for data in seperated_data:
        if data[3] == "In":
            data[3] = "In Use"
        formatted_data.append((convertTimeToSeconds(data[1][:-1]),data[2][:-1], data[0], data[3]))
    return formatted_data


def calculateOfflineOnlineTime(device_data):
    total_offline_time = 0
    total_online_time = 0
    offline_trigger = 0
    # see if a single entry is offline or online
    if len(device_data) == 1 and "Offline" in device_data[0]:
        offline_trigger = 1

    # To calculate the total offline time and total online time
    for i, list in enumerate(device_data):
        if "Offline" in list and i+1 < len(device_data):
            total_offline_time += device_data[i+1][0] - device_data[i][0]
        elif "Offline" not in list and i+1 < len(device_data):
            total_online_time += device_data[i+1][0] - device_data[i][0]

    return {"Offline time": total_offline_time, "Online time": total_online_time, "Total time": (total_online_time+total_offline_time), "Offline trigger": offline_trigger, "Device name": device_data[0][1],
    "Date": device_data[0][2]}


# data formatted into dictionary {date: [data]} format
def seperateByDate(arrayToFormat):
    dataDic = defaultdict(list)

    for data in arrayToFormat:
        dataDic[data[2]].append(data)

    return dataDic


def calculateDowntimePercent(times_to_calculate):
    time_dic = calculateOfflineOnlineTime(times_to_calculate)

    # make dict values into array to calculate percent
    list_of_times = list(time_dic.values())

    # case if it is only 1 entry
    if list_of_times[2] == 0 and list_of_times[3] == 1:
        return f"Your device {list_of_times[4]} is down {100.0}% of the time on Date: {list_of_times[5]}."
    elif list_of_times[2] == 0 and list_of_times[3] != 1:
        return f"Your device {list_of_times[4]} is down {0.0}% of the time on Date: {list_of_times[5]}."
    else:
        downtime_percent = (list_of_times[0]/list_of_times[2])*100
        downtime_message  = f"Your device {list_of_times[4]} is down {round(downtime_percent,2)}% of the time on Date: {list_of_times[5]}."
        return downtime_message


# data formatted into dictionary {device : [date: [data]]} format
def seperateDataByDeviceAndDate(arrayToFormat):
    seperated_data = seperateDataByDevice(arrayToFormat)

    final_dic = defaultdict(list)
    for arrays in seperated_data.values():
        final_dic[arrays[0][1]].append(seperateByDate(arrays))

    return final_dic


def calculateDowntimePercentPerDay(dataDic):
    final_array = []
    for array in dataDic.values():
        for dic in array:
            for info in dic.values():
                final_array.append(calculateDowntimePercent(info))

    return final_array


# test case
data = seperateDataByDeviceAndDate(entries)

a = calculateDowntimePercentPerDay(data)

for information in a:
    print(information)





    







