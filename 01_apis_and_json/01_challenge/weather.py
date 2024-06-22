import requests
import configparser
from datetime import datetime


API_URL_FOR_GEO_SEARCH = "http://api.openweathermap.org/geo/1.0/direct"
API_URL_FOR_FORCAST = "http://api.openweathermap.org/data/2.5/forecast"
con = configparser.ConfigParser()
con.read("../../../config.ini")
API_KEY = con["weather"]["API_KEY"]

def convert_to_celsius(kelvin):
    return (kelvin-273.15)

def search_city(city):
    query = f"{API_URL_FOR_GEO_SEARCH}?q={city}&limit=5&type=hour&appid={API_KEY}"
    res = requests.get(query)
    res.raise_for_status()
    res = res.json()
    if len(res)>0:
        for i, r in enumerate(res):
            print(f'{i+1}. {r["name"]}, {r["country"]}')
        print("Multiple matches found, which city did you mean?")
        while True:
            try:
                i = int(input())
                target = res[i-1]
                break
            except Exception as e:
                print(e)
                print("Invalid input. input again")
    else:
        raise Exception("No macth found. Please check if the name of the city is correct.")

    return target

def weather_forecast(lat, lon):
    res = requests.get(f"{API_URL_FOR_FORCAST}?lat={lat}&lon={lon}&appid={API_KEY}")  
    res.raise_for_status()
    res = res.json()["list"]
    # 24時間後、48時間後、…、120時間後の天候を取得
    # print(res)
    res_dic = []
    for i, r in enumerate(res):
        # print(r)
        if i%8==0:
            max_tmp = convert_to_celsius(r["main"]["temp_max"])
        else:
            max_tmp = max(convert_to_celsius(r["main"]["temp_max"]), max_tmp)

        if i%8==7:
            # print(r)
            res_dic.append({
                "date": datetime.fromtimestamp(r["dt"]).strftime("%Y-%m-%d"),
                "weather": r["weather"][0]["main"].title(),
                "max_temp": '{:.0f}°C'.format(max_tmp)
            })
    return res_dic

def main():
    city = input("City?\n")
    res = search_city(city)
    # print(res)

    res = weather_forecast(res["lat"],res["lon"])
    for r in res:
        print(f'{r["date"]}: {r["weather"]} ({r["max_temp"]})')

    # time = datetime.fromtimestamp({UNIX time})
    # res.raise_for_status()
    # return res.json()

if __name__=="__main__":
    main()