import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()  # reads variables from .env into the environment

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv("OWM_API_KEY")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

weather_params = {
    "lat": 17.516034,
    "lon": 78.432496,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 820:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's full of rainy out pls carrie umbrella ☔ 😎",
        from_=os.getenv("TWILIO_FROM_NUMBER"),
        to=os.getenv("TWILIO_TO_NUMBER"),
    )
    print(message.status)



