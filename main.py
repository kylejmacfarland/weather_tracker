from requester import Requester
import pandas as pd
import sqlite3

def to_celcius(f) -> float:
    return (f - 32.0) / 1.8

def to_fahrenheit(c) -> float:
    return c * 1.8 + 32.0

def to_kph(mph) -> float:
    return mph * 1.609344

def to_mph(kph) -> float:
    return kph / 1.609344

def retrieve_observation(latitude, longitude):
    r = Requester()
    data = r.request(f"points/{latitude},{longitude}")
    station_url = data["properties"]["observationStations"]
    forecast_url = data["properties"]["forecast"]
    # Retrieve current weather data.
    data = r.request_url(station_url)
    nearest_station = data["observationStations"][0]
    print("Current:")
    data = r.request_url(nearest_station + "/observations/latest")
    temperature = data["properties"]["temperature"]["value"]
    print(f"Temperature:\t{temperature} C, {to_fahrenheit(temperature)} F")
    windspeed = data["properties"]["windSpeed"]["value"]
    print(f"Wind Speed:\t{windspeed} KPH, {to_mph(windspeed)} MPH")
    humidity = data["properties"]["relativeHumidity"]["value"]
    print(f"Humidity:\t{humidity} %")
    precipitation = data["properties"]["precipitationLastHour"]["value"]
    print(f"Precipitation (Last Hour):\t{precipitation} mm")
    print()
    # Retrieve forecasted weather data.
    data = r.request_url(forecast_url)
    periods = data["properties"]["periods"]
    for p in periods:
        print(f"{p["name"]}:")
        print(f"{p["shortForecast"]}")
        temperature = p["temperature"]
        print(f"Temperature:\t{to_celcius(temperature)} C, {temperature} F")
        windspeed = p["windSpeed"]
        print(f"Wind Speed:\t{windspeed}")
        precipitation = p["probabilityOfPrecipitation"]["value"]
        print(f"Chance of Rain:\t{precipitation} %")
        print()

def retrieve_stations(id):
    r = Requester()
    data = r.request(f"stations?id={id}")
    df = pd.json_normalize(data, record_path="features")
    df.columns = df.columns.str.replace("properties.", "", regex=True)
    df[["xcoord", "ycoord"]] = pd.DataFrame(df["geometry.coordinates"].tolist(), index = df.index)
    df = df.drop("geometry.coordinates", axis=1)
    df = df.drop("@id", axis=1)
    df = df.drop("type", axis=1)

    conn = sqlite3.connect("db/data.db")
    df.to_sql("stations", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def query_stations():
    conn = sqlite3.connect("db/data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * from stations")
    rows = cursor.fetchall()
    for r in rows:
        print(r)

def main():
    # Retieve data from NYC
    retrieve_observation(40.7128, -74.0060)

main()
