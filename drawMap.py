import os
from datetime import date
import random
import gpxpy
import gpxpy.gpx
import time
import matplotlib.pyplot as plt

EXPORT_DIR = "./exports/"
route_info = []

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

with open('./data/data_06.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                route_info.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation
                })

def get_min_max():
    min_latitude = route_info[0]['latitude']
    max_latitude = route_info[0]['latitude']
    min_longitude = route_info[0]['longitude']
    max_longitude = route_info[0]['longitude']
    for i in range(len(route_info)):
        if route_info[i]['latitude'] < min_latitude:
            min_latitude = route_info[i]['latitude']
        if route_info[i]['latitude'] > max_latitude:
            max_latitude = route_info[i]['latitude']
        if route_info[i]['longitude'] < min_longitude:
            min_longitude = route_info[i]['longitude']
        if route_info[i]['longitude'] > max_longitude:
            max_longitude = route_info[i]['longitude']
    return min_latitude, max_latitude, min_longitude, max_longitude

def get_random_locations(num):
    random_locations = []
    for _ in range(num):
        random_locations.append(route_info[random.randint(0, len(route_info) - 1)])
    return random_locations

def draw_line():
    fig, ax = plt.subplots()
    random_locations = get_random_locations(30)
    min_latitude, max_latitude, min_longitude, max_longitude = get_min_max()
    for i in range(len(random_locations)):
        x = map(random_locations[i]['longitude'], min_longitude, max_longitude, 0, 1)
        y = map(random_locations[i]['latitude'], min_latitude, max_latitude, 0, 1)
        if i == 0:
            ax.plot(x, y, marker='o', markersize=5, color="black")
        else:
            ax.plot(x, y, marker='o', markersize=5, color="black")
            ax.plot([x_old, x], [y_old, y], color="black")
        x_old, y_old = x, y
    plt.axis('off')
    plt.savefig('map.png', bbox_inches='tight', pad_inches=0)

def make_folder_if_missing():
    today = date.today()
    folder_name = today.strftime("%b-%d-%Y")
    path = os.path.join(EXPORT_DIR, folder_name)
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path

def draw_map():
    draw_line()
    loc = make_folder_if_missing()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    os.rename('map.png', u'%s/map_%s.png' % (loc, timestr))

draw_map()
