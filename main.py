from requester import Requester
import pandas as pd

def main():
    r = Requester()
    data = r.request()
    df = pd.json_normalize(data, record_path="features")
    print(df)

main()