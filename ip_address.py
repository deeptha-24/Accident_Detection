import requests

# response = requests.get("http://ip-api.com/json/24.48.0.1").json()
# print(response)
# print(response['lat'])
# print(response['lon'])


# {"query": "167.71.3.72"},
#         {"query": "206.189.198.234"},
#         {"query": "157.230.75.212"},
def get_ip_address():
    response = requests.post("http://ip-api.com/batch", json=[
        {"query": "208.80.152.201"},


    ]).json()
    for ipinfo in response:
        lat=ipinfo['lat']
        lon=ipinfo['lon']
        return [lat,lon]