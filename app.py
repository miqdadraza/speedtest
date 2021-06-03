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
import pandas_bokeh
import os

pandas_bokeh.output_file("Interactive Plot.html")

# defining global variables:
speed_res, isp_res, speed_time = get_speed()
date_time_string = speed_time.strftime("%d/%m/%Y %H:%M")

server_info = {'time': date_time_string, 'isp': isp_res}
fname_server = 'server_info.json'
entry_server = server_info

speed_info = {'time':date_time_string, 'speeds': speed_res}
fname_speed = 'speed_info.json'
entry_speed = speed_info

def save_speed_info():
    """
    saves speed info with date/time as dict in a file
    """
    
    # solution from https://stackoverflow.com/a/35830107
    a = [] # initializes a new list for json
 
    if not os.path.isfile(fname_speed): #checks if file exists
        a.append(speed_info)
        with open(fname_speed, mode='w') as f:
            f.write(json.dumps(a, indent=4)) # uses the list, appends to list and adds to json
    else: # otheriwse opens file, reads and loads json data into a variable, appends to feeds
        with open(fname_speed) as feedsjson:
            feeds = json.load(feedsjson) # benefit here is that feeds is a list

        feeds.append(entry_speed)
        with open(fname_speed, mode='w') as f:
            f.write(json.dumps(feeds, indent=4))

def save_server_info():
    """
    saves server info with date/time as dict in a file
    """

    a = [] # initializes a new list for json
    
    if not os.path.isfile(fname_server): #checks if file exists
        a.append(server_info)
        with open(fname_server, mode='w') as f:
            f.write(json.dumps(a, indent=4)) # uses the list, appends to list and adds to json
    else: # otheriwse opens file, reads and loads json data into a variable, appends to feeds
        with open(fname_server) as feedsjson:
            feeds = json.load(feedsjson) # benefit here is that feeds is a list

        feeds.append(entry_server)
        with open(fname_server, mode='w') as f:
            f.write(json.dumps(feeds, indent=4))

def speed_df():
    """
    will read the speed file json and return it as a df
    """
    with open('speed_info.json', 'r') as f:
        data = json.loads(f.read())
    speed_df = pd.json_normalize(data)
    speed_df["time"] = pd.to_datetime(speed_df["time"])
    return speed_df

def graph_speed(speed_df):
    df = pd.DataFrame(speed_df).set_index("time").tail(10)
    df.rename(columns={'time': 'Time', 'speeds.download': 'Download Speed', 'speeds.upload': 'Upload Speed'}, inplace=True)
    df_plot_bar = df.plot_bokeh.line(
    x_axis_type='datetime',
    figsize=(800, 800),
    ylabel="Speed [Mb/s]", 
    xlabel="Date/Time",
    title="Download/Upload Speeds by Time", 
    alpha=0.6,
    vertical_xlabel=False,
    show_figure = False,
    return_html = False)

    # df_plot_line = df.plot_bokeh(kind='line', show_figure = True)

    # df_plot_line = df.plot_bokeh.line(
    # title="Download vs Upload",
    # xlabel="Date/Time",
    # ylabel="Speed [Mb/s]",
    # alpha=0.6,
    # vertical_xlabel=True,
    # show_figure=False)

    pandas_bokeh.plot_grid([[df_plot_bar]])

    
# def graph_speeds():
#     speed_info_df = pd.read_json(path_or_buf='speed_info_text.json', lines=True)
#     return speed_info_df

def main():
    save_speed_info()
    save_server_info()
    df = speed_df()
    graph_speed(df)


    # print(graph_speeds())
    # print(speed_res)
    # print(isp_res)
    # print(speed_time)
    

if __name__ == '__main__':
    main() 