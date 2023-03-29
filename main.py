import time
import cv2
import requests
from googleplaces import GooglePlaces, types, lang
import requests
import threading
import json
from flask import Flask, render_template, url_for, flash, redirect, Response, jsonify
from datetime import datetime
from flask_bootstrap import Bootstrap
# from camera import Camera
from ip_address import get_ip_address
# from location_hospital import get_location
from detection import AccidentDetectionModel
import numpy as np
import os
from forms import LoginForm
global ip_address, lat, lon, query_result
model = AccidentDetectionModel("model.json", '123.h5')
font = cv2.FONT_HERSHEY_SIMPLEX
import pandas as pd
import math
import random
#

from twilio.rest import Client
app = Flask(__name__)
account_sid =  'ACf7b85428cff4b8d53fb51ea70c2f2df5'
auth_token = 'c4bd446ad6657f6025bb7ed26ca407ec'

# API_KEY = 'AIzaSyBPNgFZT6ZUIN2Wsrk3GOSgo67NAKseTIA'
# google_places = GooglePlaces(API_KEY)

app.secret_key = "akanksha"
Bootstrap(app)

l=[]

class Camera(object):

    def __init__(self):
        self.video = cv2.VideoCapture('cars6.mp4')
        self.accident_prob = 0


    def probability(self):

        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))
            pred, prob = model.predict_accident(roi[np.newaxis, :, :])

            if pred == "Accident":
                prob = (round(prob[0][0] * 100, 2))
                if prob>=95:
                    l.append(prob)
                    break

        return l



    def startapplication(self):

        while True:
            ret, frame = self.video.read()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))

            pred, prob = model.predict_accident(roi[np.newaxis, :, :])
            if pred == "Accident":
                prob = (round(prob[0][0] * 100, 2))

                if prob>=99:
                    print("Alert Hospital")
                    #self.accident_prob = 1
                    print(prob)


            ret, jpg = cv2.imencode('.jpg', frame)
            return jpg.tobytes()

camera = Camera()
def gen():

    while True:
        frame = camera.startapplication()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.username.data == 'admin' and login_form.password.data == 'ab':
            return render_template('accident_page.html')

    return render_template('login.html', form=login_form)


@app.route('/accident_page')
def accident_page():

    return render_template('accident_page.html')


def detected():
    a = camera.probability()
    print(a)
    for prob in a:
        if prob >= 95:
            # time.sleep(5)
            return prob/100


@app.route('/accident_detected')

def accident_detected():
    i = random.randint(1,4)
    if i==1:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "208.80.152.201"},
        ]).json()
    if i==2:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "192.168.0.119"},
        ]).json()
    if i == 3:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "223.186.17.128"},
        ]).json()
    if i == 4:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query":  "223.231.183.75"},
        ]).json()



    for ipinfo in response:
        lat = ipinfo['lat']
        lon = ipinfo['lon']
        location = (lat, lon)
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body = f"Accident Detected. Latitude:{lat}, Longitude:{lon} ",
            from_ = "+15074458887", 
            to = "+919739561820"
        )
        print(message.sid)
        radius = 10  # radius in kilometers
        nearby_hospitals_all = get_nearby_hospitals(location[0], location[1], radius)
        nearby_hospitals_all=nearby_hospitals_all[0:3]
        return render_template('accident_detected.html', ip_address_lat=lat,
                               ip_address_lon=lon, nearby_hospitals_all=nearby_hospitals_all)

# @app.route('/accident_prob')
# def accident_prob():
#     accident_prob = detected()
#     return jsonify({'accident_prob': accident_prob})


@app.route('/get_accident_probability')
def get_accident_probability():
    accident_prob=detected()
    return jsonify(accident_prob=accident_prob)

# threshold=0.9
# @app.route('/check_probability')
# def check_probability():
#
#     probability = detected() # simulate probability changing over time
#     return jsonify(visible=(probability > threshold))

# @app.route("/get_probability")
# def get_probability():
#     probability = detected()# code to get current probability value
#     return jsonify(probability=probability)

hospitals_df = pd.read_csv('hospitals1.csv')
def distance(lat1, lon1, lat2, lon2):
    # convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # calculate the distance using Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371 # radius of Earth in kilometers
    return c * r


# define a function to get nearby hospitals
def get_nearby_hospitals(latitude, longitude, radius):
    nearby_hospitals = []
    for index, row in hospitals_df.iterrows():
        hospital_latitude = row['LATITUDE']
        hospital_longitude = row['LONGITUDE']
        hospital_distance = distance(latitude, longitude, hospital_latitude, hospital_longitude)
        if hospital_distance <= radius:
            nearby_hospitals.append(row['NAME'])
    return nearby_hospitals


if __name__ == '__main__':

    app.run(debug=True)
    