import requests
from io import BytesIO
from PIL import Image


def get_image(lon, lat, delta, view="map"):
    req_url = f"http://static-maps.yandex.ru/1.x/"
    params = {
        "ll": ",".join((lon, lat)),
        "spn": ",".join((delta, delta)),
        "l": view
    }
    response = requests.get(req_url, params=params)
    stream = BytesIO(response.content)
    return Image.open(stream)


def get_toponym_coords(toponym_name):
    req_url = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_name,
        "format": "json"
    }
    response = requests.get(req_url, params=params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"] \
        ["featureMember"][0]["GeoObject"]
    toponym_coords = toponym["Point"]["pos"]
    return toponym_coords.split(" ")
