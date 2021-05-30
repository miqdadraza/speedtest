"""
    This python application will test your internet speed, and email and text it to you.
    In addition, it will also store the date/time, and the upload speed, download speed, and ping to a file.
    From this file, it will generate an interactive graph, and save this graph as html.
    You will also get this graph in your email.

"""

"""
    Psuedocode:
    1) Speed:
        a. Get ping and store it in a variable.
        b. Get upload speed and store it in a variable.
        c. Get download speed and store it in a variable.
"""

#import speedtest
from speedtest_get import get_speed
import json
from datetime import datetime
import pandas as pd
import pandas_bokeh as pb
import os

# defining global variables:
speed_res, isp_res, speed_time = get_speed()
date_time_string = speed_time.strftime("%d/%m/%Y %H:%M")

def save_speed_info():
    """
    saves speed info with date/time as dict in a file
    """
    speed_info = {'time':date_time_string, 'speeds': speed_res}
    
    # solution from https://stackoverflow.com/a/35830107
    a = [] # initializes a new list for json
    fname = 'speed_info.json'
    entry = speed_info

    if not os.path.isfile(fname): #checks if file exists
        a.append(speed_info)
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=2)) # uses the list, appends to list and adds to json
    else: # otheriwse opens file, reads and loads json data into a variable, appends to feeds
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson) # benefit here is that feeds is a list

        feeds.append(entry)
        with open(fname, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

def save_server_info():
    """
    saves server info with date/time as dict in a file
    """
    server_info = {'time': date_time_string, 'isp': isp_res}
    with open('isp_info_txt', 'a') as f:
        f.write(json.dumps(server_info) + "\n")

# def graph_speeds():
#     speed_info_df = pd.read_json(path_or_buf='speed_info_text.json', lines=True)
#     return speed_info_df

def main():
    save_speed_info()
    save_server_info()

    # print(graph_speeds())
    # print(speed_res)
    # print(isp_res)
    # print(speed_time)
    

if __name__ == '__main__':
    main() 