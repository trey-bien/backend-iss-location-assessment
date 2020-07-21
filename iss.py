#!/usr/bin/env python

import requests
import time
import turtle

__author__ = 'Trey Dickerson'

passover_risetime = 0
iss_long = 0
iss_lat = 0
iss_timestamp = 0

def astronaut_list():
    r = requests.get('http://api.open-notify.org/astros.json')
    data = r.json()
    astros = data['people']
    print('Number of Astronauts in space: ', len(astros))
    print('Astronauts in Space:')
    for astro in astros:
        print('Name:', astro['name'])
        print('Craft:', astro['craft'])
    return

def current_iss_coords():
    r = requests.get('http://api.open-notify.org/iss-now.json')
    data = r.json()
    global iss_long
    global iss_lat
    global iss_timestamp
    iss_coords = data['iss_position']
    iss_long = iss_coords['longitude']
    iss_lat = iss_coords['latitude']
    iss_timestamp = data['timestamp']
    
    print('ISS CURRENT TIME/LOCATION')
    print('Timestamp: ', iss_timestamp)
    print('Longitude: ', iss_long)
    print('Latitude: ', iss_lat)
    return

def create_map():
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic('map.gif')
    screen.register_shape('iss.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)

    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)

    iss.penup()
    iss.goto(float(iss_long), float(iss_lat))
    iss.pendown()

    indy_long = -86.2
    indy_lat = 39.8
    indianapolis = turtle.Turtle()
    indianapolis.shape('circle')
    indianapolis.color('yellow')
    indianapolis.setheading(90)
    indianapolis.penup()
    indianapolis.goto(float(indy_long), float(indy_lat))
    style = ('Courier', 12)
    indianapolis.write('Next ISS passover for\nIndianapolis is\n' +
                   passover_risetime + '.', font=style, align='left')
    
    turtle.done()

def next_pass():
    r = requests.get(
        'http://api.open-notify.org/iss-pass.json?lat=39.7684&lon=-86.1581')
    data = r.json() 
    global passover_risetime
    passover_risetime = time.ctime(
        data['response'][0]['risetime'])
    print("The next time the ISS will pass over Indianapolis is", passover_risetime)
    return 



def main():
    astronaut_list()
    current_iss_coords()
    next_pass()
    create_map()


if __name__ == '__main__':
    main()
