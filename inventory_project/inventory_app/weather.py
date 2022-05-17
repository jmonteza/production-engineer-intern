import requests


def get_city_weather(city):
    '''
    Returns the name, temperature, pressure, and humidity of the city

            Parameters:
                    city (str): The city we want to search for weather

            Returns:
                    A tuple containing name (name of the city), temperature (temperature of the city), pressure (pressure of the city), and humidity (humidity of the city).
    '''
    geo_response = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct?q={},CA&limit=5&appid={}".format(city, "e3967737f54ceb090c8c7e0ea77e9eea"))

    lat = geo_response.json()[0].get("lat")
    lon = geo_response.json()[0].get("lon")

    weather_response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, "e3967737f54ceb090c8c7e0ea77e9eea"))

    name = weather_response.json().get("name")
    temperature = weather_response.json().get("main").get("temp")
    pressure = weather_response.json().get("main").get("pressure")
    humidity = weather_response.json().get("main").get("humidity")

    return (name, temperature, pressure, humidity)
