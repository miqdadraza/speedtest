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
from email import encoders
from bokeh.io import export_png
import matplotlib.pyplot as plt
import seaborn as sns


pandas_bokeh.output_file("InteractivePlot.html")

# defining global variables:
speed_res, isp_res, speed_time = get_speed()
date_time_string = speed_time.strftime("%d/%m/%Y %H:%M")

server_info = {'time': date_time_string, 'isp': isp_res}
fname_server = 'server_info.json'
entry_server = server_info

speed_info = {'time':date_time_string, 'speeds': speed_res}
fname_speed = 'speed_info.json'
entry_speed = speed_info

from_email = 'miqdadraza.bhurani@gmail.com'
email_pass = 'Superman<3'

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
    df_plot_bar = df.plot_bokeh.bar(
    figsize=(800, 800),
    ylabel="Speed [Mb/s]", 
    xlabel="Date/Time",
    title="Download/Upload Speeds by Time", 
    alpha=0.6,
    vertical_xlabel=True,
    show_figure = False,
    return_html = True)
    # export_png(df_plot_bar, filename='plot.png')
    return df_plot_bar

    # df_plot_line = df.plot_bokeh.line(
    # title="Download vs Upload",
    # xlabel="Date/Time",
    # ylabel="Speed [Mb/s]",
    # alpha=0.6,
    # vertical_xlabel=True,
    # show_figure=False)

    # pandas_bokeh.plot_grid([[df_plot_bar]])
    
    
# def graph_speeds(speed_df):
#     # df = pd.DataFrame(speed_df).set_index("time").tail(10)
#     df = pd.DataFrame(speed_df)

#     #df.rename(columns={'time': 'Time', 'speeds.download': 'Download Speed', 'speeds.upload': 'Upload Speed'}, inplace=True)
#     data_speeds = sns.load_dataset(df) 
#     f, ax = plt.subplots(1,1)
#     sns.barplot(data=data_speeds, x="time")
#     plt.show()





def generate_html(up, down, graphed_speed):
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
            <p align="center"><strong>A graphical representation of the last 10 speed points is below:</strong></p>
            {}
            
                
                
            </p>
    </body>
</html>
    """.format(datetime.now().strftime('%m/%d/%Y %H:%M') ,up, down, graphed_speed)
    with open('final_email.html', 'w') as f:
        f.write(html_text)
    
    
    


def speeds():
    down = "{:.2f}".format(speed_res['download'])
    upload = "{:.2f}".format(speed_res['upload'])
    return down, upload

def send_email():
    # smtp_server = 'smtp-mail.outlook.com'
    # smtp_tls = 587
    # to_email = 'miqdad.accounts@bhurani.net'

    # with open('final_email.html', 'r') as f:
    #     data = f.read()
    # email_body = "Subject: Your Internet Speeds\n\n" + data

    # smtpObj = smtplib.SMTP(smtp_server, smtp_tls)
    # smtpObj.ehlo()
    # smtpObj.starttls()
    # smtpObj.login(from_email, email_pass)
    # smtpObj.sendmail(from_email, to_email, email_body)
    # smtpObj.quit()
    pass



def main():
    save_speed_info()
    save_server_info()
    df = speed_df()
    # df.rename(columns={'time': 'Time', 'speeds.download': 'Download Speed', 'speeds.upload': 'Upload Speed'}, inplace=True)
    # fig, ax = plt.subplots()
    # ax.bar(x=df['Time'], height = df['Download Speed'], label = 'Download Speed')
    # ax.bar(x=df['Time'], height = df['Upload Speed'], label = 'Upload Speed')

    # plt.show()
    
    
    
    up, down = speeds()
    graphed_speed = graph_speed(df)
    generate_html(up, down, graphed_speed)
    # send_email()
    smtp_server = 'smtp.gmail.com'
    smtp_tls = 587
    to_email = 'miqdad.accounts@bhurani.net'

    with open('final_email.html', 'r') as f:
        data = f.read()
    email_body = "Subject: Your Internet Speeds\n\n" + data

    message = MIMEMultipart()
    html_part = MIMEText(data, 'html')
    message.attach(html_part)
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("Interactive Plot.html", "rb").read())
    encoders.encode_base64(part)
    
    part.add_header('Content-Disposition', 'attachment; filename="Interactive Plot.html"')
    message.attach(part)
    # print(message.as_string())

    smtpObj = smtplib.SMTP(smtp_server, smtp_tls)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(from_email, email_pass)
    smtpObj.sendmail(from_email, to_email, message.as_string())
    smtpObj.quit()

    



    


    

    # print(graph_speeds())
    # print(speed_res)
    # print(isp_res)
    # print(speed_time)
    

if __name__ == '__main__':
    main() 