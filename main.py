import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Uses the openweathermap api to get data
OWM_Endpointer = "https://api.openweathermap.org/data/2.5/onecall"
# Hides personal keys within env
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    # New York
    "lat": 40.712776,
    "lon": -74.005974,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpointer, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice_1 = weather_data["hourly"][:12]

thunder_storm = False
rain = False
snow = False

for hours in weather_slice_1:
    condition_code = hours["weather"][0]["id"]
    if int(condition_code) < 300:
        thunder_storm = True
    elif int(condition_code) > 299 and int(condition_code) < 600:
        snow = True
    elif int(condition_code) > 599 and int(condition_code) < 700:
        rain = True

if thunder_storm:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body = "It's going to thunderstorm today ⛈",
            # removed phone numbers
            from_ = " #", 
            to = " #",
        )
    print(message.status)

if rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body = "It's going to rain today, bring an umbrella ☂️",
            from_ = " #",
            to = " #",
        )
    print(message.status)

if snow:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body = "It's going to snow today! 🌨️ ❄️",
            from_ = " #",
            to = " #",
        )
    print(message.status)
