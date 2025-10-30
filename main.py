from requester import Requester
import pandas as pd
import sqlite3

def to_fahrenheit(c) -> float:
    return c * 1.8 + 32.0

def to_mph(kph) -> float:
    return kph * 0.621371

def retrieve_observation(latitude, longitude):
    r = Requester()
    data = r.request(f"points/{latitude},{longitude}")
    station_url = data["properties"]["observationStations"]
    data = r.request_url(station_url)
    nearest_station = data["observationStations"][0]
    print(nearest_station+"/observations/latest")
    data = r.request_url(nearest_station + "/observations/latest")
    temperature = data["properties"]["temperature"]["value"]
    print(f"Temperature:\t{temperature} C, {to_fahrenheit(temperature)} F")
    windspeed = data["properties"]["windSpeed"]["value"]
    print(f"Wind Speed:\t{windspeed} KPH, {to_mph(windspeed)} MPH")
    humidity = data["properties"]["relativeHumidity"]["value"]
    print(f"Humidity:\t{humidity} %")
    precipitation = data["properties"]["precipitationLastHour"]["value"]
    print(f"Precipitation (Last Hour):\t{precipitation} mm")

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
