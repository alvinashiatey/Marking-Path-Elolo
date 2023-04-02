import os
from datetime import date
import random
import drawBot
import gpxpy
import gpxpy.gpx
import time

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

# [{'latitude': 6.687664, 'longitude': -1.556504, 'elevation': 270.73639}, {'latitude': 6.687639, 'longitude': -1.556501, 'elevation': 270.77425}, {'latitude': 6.687679, 'longitude': -1.556517, 'elevation': 270.78563}, {'latitude': 6.687745, 'longitude': -1.556522, 'elevation': 270.78601}] 
#  A function that randomly selects 5 points from route_info and draws a line between them 
#  The line is drawn from the first point to the last point

# A function to find the minimum and maximum values ​​of latitude and longitude
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
        random_locations = get_random_locations(30)
        drawBot.stroke(0)
        drawBot.strokeWidth(2)
        drawBot.fill(None)
        min_latitude, max_latitude, min_longitude, max_longitude = get_min_max()
        drawBot.newPath()
        for i in range(len(random_locations)):
                x = map(random_locations[i]['longitude'], min_longitude, max_longitude, 0, drawBot.width())
                y = map(random_locations[i]['latitude'], min_latitude, max_latitude, 0, drawBot.height())
                if i == 0:
                        drawBot.moveTo((x, y))
                else:
                        drawBot.lineTo((x, y))
        drawBot.closePath()
        drawBot.drawPath()


def new_page():
        drawBot.newPage(1000, 1000)
        drawBot.fill(0.99)
        drawBot.rect(0, 0, drawBot.width(), drawBot.height())
        drawBot.fill(0)

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
        new_page()
        draw_line()
        loc = make_folder_if_missing()
        timestr = time.strftime("%Y%m%d-%H%M%S")
        options = dict(
                multipage=False
        )
        drawBot.saveImage(u'%s/map_%s.png' % (loc, timestr), **options)

draw_map()