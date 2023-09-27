import json
from datetime import datetime
from pprint import pprint

import requests

import config
from db import queries as sql


def get_weather():
    data = []

    username = input('username: ')

    if not sql.check_user_exists("weather.db", username):
        # sql.add_user("weather.db", username)
        sql.add_data("weather.db", "users", username=username)
        print("user added: ", username)
        get_weather()
    else:
        user_id = sql.get_user_id("weather.db", username=username)
        while True:
            city = input("Введите город, в котором хотите узнать погоду: ")

            if city == "show":
                data = sql.get_user_weather("weather.db", user_id)
                for item in data:
                    print(item)
                continue
            if city == "save":
                with open("weather.json", mode="w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                continue

            config.parameters["q"] = city

            resp = requests.get(config.url, params=config.parameters).json()
            pprint(resp)  # dt, name, sunrise, sunset, description, speed

            tz = resp["timezone"]
            dt = datetime.utcfromtimestamp(resp["dt"] + tz).strftime("%H:%M:%S")

            name = resp["name"]
            sunrise = datetime.utcfromtimestamp(resp["sys"]["sunrise"] + tz).strftime("%H:%M:%S")
            sunset = datetime.utcfromtimestamp(resp["sys"]["sunset"] + tz).strftime("%H:%M:%S")
            description = resp["weather"][0]["description"]
            speed = resp["wind"]["speed"]
            temp = resp["main"]["temp"]

            sql.add_data("weather.db", "weather",
                         name=name,
                         tz=tz,
                         dt=dt,
                         sunrise=sunrise,
                         sunset=sunset,
                         description=description,
                         temp=temp,
                         speed=speed,
                         user_id=user_id
                         )

            data.append({
                "name": name,
                "sunrise": sunrise,
                "sunset": sunset,
                "description": description,
                "temp": temp,
                "speed": speed
            })

            print(f"""
В городе {name} сейчас {description}
Температура: {temp}
Скорость ветра: {speed}
Восход: {sunrise}
Закат: {sunset}
Время запроса: {dt}
""")
