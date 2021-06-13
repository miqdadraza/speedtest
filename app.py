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
from itertools import groupby
from speedtest_get import get_speed
import json
from datetime import datetime
import pandas as pd
import pandas_bokeh
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

from email import encoders
# from bokeh.io import export_png
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTickFormatter
from getpass import getpass

from_email = 'miqdadraza.bhurani@gmail.com'
# email_pass = 'Superman<3'

output_file("InteractivePlot_main.html")

# defining global variables:
speed_res, isp_res, speed_time = get_speed()
date_time_string = speed_time.strftime("%m/%d/%Y %H:%M")

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
    speed_df["time"] = pd.to_datetime(speed_df["time"], format="%m/%d/%Y %H:%M")
    return speed_df

    
def graph_mpl(df):
    fig, ax = plt.subplots()
    ax.plot(df["time"], df["speeds.download"], label = "Download", color='blue', marker='o', linestyle = '-')
    ax.plot(df["time"], df["speeds.upload"], label = "Upload", color='red', marker='x', linestyle = '-')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.xticks(rotation=45)
    plt.xticks(df['time'])
    plt.title("Download/Upload Speeds")
    plt.xlabel("Date/Time")
    plt.ylabel("Speed (Mb/s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fname = "Up_Down_Speeds.png")
    
    
def generate_html(up, down, servers_email):
    html_text = r"""<html>
    <body>
        <h1>The following is information about your internet speed:</h1>
        <body>
        <p align="center"><strong>The current time is: </strong> {}
            <p align="center"><strong>Your current speeds are:</strong>
            <br>
                <strong>Download</strong> = {} Mbps
                <br>
                <strong>Upload</strong> = {} Mbps
                <br>
            </br>

            <p align="center"><strong>The server information is:</strong></p>
            <p align="center">{}</p>
            <p align="center"><strong>A graphical representation of the last few speed points is attached to this email.</strong></p>
              
            </p>
    </body>
</html>
    """.format(datetime.now().strftime('%m/%d/%Y %H:%M') ,up, down, servers_email)
    with open('final_email.html', 'w') as f:
        f.write(html_text)


def speeds():
    down = "{:.2f}".format(speed_res['download'])
    upload = "{:.2f}".format(speed_res['upload'])
    return down, upload

def email_to():
    smtp_server = 'smtp.gmail.com'
    smtp_tls = 587
    to_email = 'miqdad.accounts@bhurani.net'

    with open('final_email.html', 'r') as f:
        data = f.read()
    # email_body = "Subject: Your Internet Speeds\n\n" + data

    message = MIMEMultipart()
    text_part = "Subject: Your Internet Speeds\n\n"
    html_part = MIMEText(data, 'html')
    # message.attach(text_part)
    message.attach(html_part)
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("Up_Down_Speeds.png", "rb").read())
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', 'attachment; filename="Up_Down_Speeds.png"')
    message.attach(part)
    message['Subject'] = "Your Internet Speeds"
    with open("password.txt", "r") as f:
        email_pass = f.read()
    # email_pass = getpass("Please input the email password: ")
    smtpObj = smtplib.SMTP(smtp_server, smtp_tls)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(from_email, email_pass)
    smtpObj.sendmail(from_email, to_email, message.as_string())
    smtpObj.quit()

def servers_email():
    servers_email_str = ""
    for i in server_info['isp']:
        servers_email_str+= str(i) + " --> " + str(server_info['isp'][i]) + "</br>"
    return servers_email_str

def main():
    save_speed_info()
    save_server_info()
    df = speed_df()
    up, down = speeds()
    graph_mpl(df.tail(10))
    servers_email_ = servers_email() 
    generate_html(up, down, servers_email_)
    email_to()
   

if __name__ == '__main__':
    main() 