"""
This file will generate the down + up speed and the ping
"""
import speedtest

def get_speed():
    s = speedtest.Speedtest()
    best_server = s.get_best_server()
    down_speed = s.download()
    up_speed = s.upload(pre_allocate=False) # to avoid memory error
    results = s.results.dict()
    return results

