import requests
from bs4 import BeautifulSoup
import json
import sys
import data_write as dw


def json_to_param(json_data):
    param = "?"
    for p in json_data.keys():
        param += p + "=" + json_data[p] + "&"
    return param

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    return soup

def main():
    args = sys.argv
    for i in range(2, len(args)):
        args[1] += args[i]
    json_data = dw.json_to_dict("company.json")
    if not args[1] in json_data.keys():
        print("以下の企業の中から選択してください")
        for c_name in json_data.keys():
            print(c_name)
        return
    soup1 = get_soup(json_data[args[1]])
    data = {}
    data["title"] = soup1.title.string
    dw.dict_to_json("log.json", data)

if __name__ == "__main__":
    main()