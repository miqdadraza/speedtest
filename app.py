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
    
    # with open('speed_info.json', 'a+') as f: #initializing file if it doesn't exist
    #     f.write("")
    
    a = []
    fname = 'speed_info.json'
    entry = speed_info
    if not os.path.isfile(fname):
        a.append(speed_info)
        with open(fname, mode='w') as f:
            f.write(json.dumps(a, indent=2))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)

        feeds.append(entry)
        with open(fname, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))



    # if os.stat('speed_info.json').st_size == 0:
    #     print('empty') #checking if file is empty
    #     with open('speed_info.json', 'a+') as f:
    #         json.dump(speed_info, f)
    # else:
    #     with open('speed_info.json') as f:
    #         data = json.load(f)
    #     data.update(speed_info)
    #     print(data)
    #     with open('speed_info.json', 'a+') as f:
    #         json.dump(data, f)



    #with open('speed_info.json')
    
    # with open('speed_info_text.json', mode='a') as f:
    #     json.dump(speed_info, f, indent=4)
    #     # f.write("\n")

# import json

# a_dict = {'new_key': 'new_value'}

# with open('test.json') as f:
#     data = json.load(f)

# data.update(a_dict)

# with open('test.json', 'w') as f:
#     json.dump(data, f)


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