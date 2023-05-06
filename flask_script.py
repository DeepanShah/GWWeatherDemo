from flask import Flask
import os
from dotenv import load_dotenv
import requests
import datetime
from datetime import date
import io
from matplotlib.figure import Figure
import base64

app = Flask(__name__)

@app.route('/')
def index():
    load_dotenv()

    API_KEY = os.getenv("API_KEY")

    time_now = str(date.today() - datetime.timedelta(days=1))
    time_before = str(date.today() - datetime.timedelta(days=8))

    phoenix_response = requests.get(f'http://api.weatherapi.com/v1/history.json?key={API_KEY}&q=Phoenix&dt={time_before}&end_dt={time_now}')
    phoenix_json = phoenix_response.json()

    sf_response = requests.get(f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q=San Francisco&dt={time_before}&end_dt={time_now}")
    sf_json = sf_response.json()

    dallas_response = requests.get(f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q=Dallas&dt={time_before}&end_dt={time_now}")
    dallas_json = dallas_response.json()

    def getTempHum(json_file):
        temp = []
        hum = []
        for i in range(7):
            for j in range(24):
                hourly_dict = json_file["forecast"]["forecastday"][i]["hour"][j]
                temp.append(hourly_dict["temp_f"])
                hum.append(hourly_dict["humidity"])
        return temp, hum

    phoenix_temp, phoenix_hum = getTempHum(phoenix_json)

    fig = Figure()
    (axs1, axs2) = fig.subplots(1,2)
    axs1.plot(list(range(24*7)), phoenix_temp, "-.", color="firebrick")
    axs1.set(xlabel="Hours", ylabel="Degrees Fahrenheit", title=f"Temperature in Phoenix from {time_before} to {time_now}")
    axs2.plot(list(range(24*7)), phoenix_hum, "-.", color="cornflowerblue")
    axs2.set(xlabel="Hours", ylabel="Humidity",  title=f"Humidity in Phoenix from {time_before} to {time_now}")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response1 = f"<img src='data:image/png;base64,{data}'/>\n"


    sf_temp, sf_hum = getTempHum(sf_json)
    fig = Figure()
    (axs1, axs2) = fig.subplots(1,2)
    axs1.plot(list(range(24*7)), sf_temp, "-.", color="firebrick")
    axs1.set(xlabel="Hours", ylabel="Degrees Fahrenheit", title=f"Temperature in SF from {time_before} to {time_now}")
    axs2.plot(list(range(24*7)), sf_hum, "-.", color="cornflowerblue")
    axs2.set(xlabel="Hours", ylabel="Humidity",  title=f"Humidity in SF from {time_before} to {time_now}")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response2 = f"<img src='data:image/png;base64,{data}'/>\n"

    dallas_temp, dallas_hum = getTempHum(dallas_json)
    fig = Figure()
    (axs1, axs2) = fig.subplots(1,2)
    axs1.plot(list(range(24*7)), dallas_temp, "-.", color="firebrick")
    axs1.set(xlabel="Hours", ylabel="Degrees Fahrenheit", title=f"Temperature in Dallas from {time_before} to {time_now}")
    axs2.plot(list(range(24*7)), dallas_hum, "-.", color="cornflowerblue")
    axs2.set(xlabel="Hours", ylabel="Humidity",  title=f"Humidity in Dallas from {time_before} to {time_now}")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    response3 = f"<img src='data:image/png;base64,{data}'/>"

    return response1 + response2 + response3

if __name__ == '__main__':
    app.run()