"""
This file will generate the down + up speed and the ping
"""
import speedtest
from datetime import datetime

def get_speed():
    """no inputs needed. this function will generate the speeds + ping + server info and time.
    """
    s = speedtest.Speedtest()
    # uncomment 3 lines below before production
    best_server = s.get_best_server()
    down_speed = s.download()
    up_speed = s.upload(pre_allocate=False) # to avoid memory error
    # results = {'download': 9033861.607104799, 'upload': 1257947.650452241, 'ping': 32.231, 'server': {'url': 'http://las-vegas2.speedtest.centurylink.net:8080/speedtest/upload.php', 'lat': '36.1760', 'lon': '-115.1370', 'name': 'Las Vegas, NV', 'country': 'United States', 'cc': 'US', 'sponsor': 'CenturyLink - 2', 'id': '16446', 'host': 'las-vegas2.speedtest.centurylink.net:8080', 'd': 16.43992630055811, 'latency': 32.231}, 'timestamp': '2021-05-29T22:56:59.630043Z', 'bytes_sent': 2605056, 'bytes_received': 11428416, 'share': None, 'client': {'ip': '185.242.5.82', 'lat': '36.2973', 'lon': '-115.2418', 'isp': 'M247 Ltd', 'isprating': '3.7', 'rating': '0', 'ispdlavg': '0', 'ispulavg': '0', 'loggedin': '0', 'country': 'US'}}
    results = s.results.dict()
    speed_data = {i: results[i]/1e+6 for i in list(results)[:2]}
    isp_data = results['server']
    datetime_now = datetime.now()
    return speed_data, isp_data, datetime_now

# first2pairs = {k: mydict[k] for k in list(mydict)[:2]}