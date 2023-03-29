import requests
global lat
global lon

import pandas as pd
import math

response = requests.post("http://ip-api.com/batch", json=[
        {"query": "208.80.152.201"},

    ]).json()

for ipinfo in response:
        lat = ipinfo['lat']
        lon = ipinfo['lon']
# read the CSV file containing hospitals' data
hospitals_df = pd.read_csv('hospitals.csv')


# define a function to calculate the distance between two points
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


# test the function
location = (lat, lon)
radius = 10 # radius in kilometers
nearby_hospitals_all = get_nearby_hospitals(location[0], location[1], radius)
print(nearby_hospitals_all[0:3])


    #   <script>
    #     var updateInterval = 1;
    #     var warningThreshold = 0.9; // probability threshold for warning
    #
    #     $(document).ready(function() {
    #         setInterval(updateProbability, updateInterval);
    #     });
    #
    #     function updateProbability() {
    #         $.get('/get_probability', function(data) {
    #             var probability = data.probability;
    #             if (probability > warningThreshold) {
    #                <a href="{{ url_for('accident_detected') }}" class="button primary">Accident Details</a>
	# 						 } else {
    #                 $('#content').html('<p>Probability of accident is low.</p>');
    #             }
    #         });
    #     }
    # </script>




#
# <!--								<button id="alert-button" class="danger-alert" style="display:none;">Accident Alert</button>-->
#
# <!--<button id="alert-button" class="{{ button_class }}">Accident Alert</button>-->
# <!--		<button id="accident-button" class="btn btn-default">Accident Alert</button>-->
#
# <!--<script>-->
# <!--    setInterval(() => {-->
# <!--        fetch("/get_probability")-->
# <!--        .then(res => res.json())-->
# <!--        .then(data => {-->
# <!--            const threshold = 0.9; // set your threshold here-->
# <!--            if (data.probability > threshold) {-->
# <!--                document.getElementById("accident-button").classList.remove("btn-default");-->
# <!--                document.getElementById("accident-button").classList.add("btn-danger");-->
# <!--            } else {-->
# <!--                document.getElementById("accident-button").classList.remove("btn-danger");-->
# <!--                document.getElementById("accident-button").classList.add("btn-default");-->
# <!--            }-->
# <!--        });-->
# <!--    }, 1000);-->
# <!--</script>-->