from requester import Requester
import pandas as pd
import sqlite3

def retrieve_stations():
    r = Requester()
    data = r.request()
    df = pd.json_normalize(data, record_path="features")
    df.columns = df.columns.str.replace("properties.", "", regex=True)
    df[["xcoord", "ycoord"]] = pd.DataFrame(df["geometry.coordinates"].tolist(), index = df.index)
    df = df.drop("geometry.coordinates", axis=1)
    df = df.drop("@id", axis=1)
    df = df.drop("type", axis=1)
    
    conn = sqlite3.connect("db/stations.db")
    df.to_sql("stations", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def main():
    retrieve_stations()

main()
