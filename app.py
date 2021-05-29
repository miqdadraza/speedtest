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

# defining global variables:
speed_res, isp_res, speed_time = get_speed()

def save_speed_info():
    speed_info = {speed_time.strftime("%d/%m/%Y %H:%M"): speed_res}
    with open('speed_info_text', mode='a') as f:
        f.write(json.dumps(speed_info) + "\n")


def main():
    save_speed_info()
    # print(speed_res)
    # print(isp_res)
    # print(speed_time)
    

if __name__ == '__main__':
    main() 