import requests

geo_response = requests.get(
    "https://api.openweathermap.org/geo/1.0/direct?q=London,CA&limit=5&appid={}".format("e3967737f54ceb090c8c7e0ea77e9eea"))

lat = geo_response.json()[0].get("lat")
lon = geo_response.json()[0].get("lon")

# print(geo_response.json())

weather_response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(lat, lon, "e3967737f54ceb090c8c7e0ea77e9eea"))

temperature = weather_response.json().get("main").get("temp")
pressure = weather_response.json().get("main").get("pressure")
humidity = weather_response.json().get("main").get("humidity")

print(temperature)
print(pressure)
print(humidity)