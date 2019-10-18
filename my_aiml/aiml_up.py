import aiml
import MeCab
import re
import requests
from bs4 import BeautifulSoup
import json
import data_write as dw
import data_search as ds

def main():
    k = aiml.Kernel()
    k.learn("std-startup.xml")
    k.respond("load aiml b")
    m = MeCab.Tagger ("-Owakati")
    empty = {}
    dw.dict_to_json("wish.json", empty)
    dw.dict_to_json("company.json", empty)
    while True:
        msg = m.parse(input("> "))
        if re.search("検索", msg):
            print("少々お待ちください。")
            json_data = dw.json_to_dict("wish.json")
            url = ds.json_to_param(json_data)
            search_company(url)
        print(k.respond(msg))

def search_company(url):
    soup1 = ds.get_soup('https://employment.en-japan.com/search/search_list/' + url)
    links = []
    company_list = {}
    for a1 in soup1.find_all("a"):
        link1 = a1.get("href")
        pattern = r'/desc_\d+?/$'
        if re.search(pattern, link1):
            soup2 = ds.get_soup('https://employment.en-japan.com' + link1)
            for a2 in soup2.find_all("a"):
                link2 = a2.get("href")
                if link2 in links:
                    continue
                links.append(link2)
                pattern = r'クチコミ情報'
                if re.match(pattern, a2.get_text()):
                    link3 = re.sub(r'/\?WorkID=\d+\&arearoute=$', '', link2)
                    if link3 in links:
                        continue
                    links.append(link3)
                    soup3 = ds.get_soup('https://employment.en-japan.com' + link3)
                    company_name = re.sub(r'（\d+?）の転職・求人情報｜【エンジャパン】のエン転職', '', soup3.title.string) 
                    company_list[company_name] = 'https://employment.en-japan.com' + link3
                    #print(company_name)
                    if len(company_list) == 5:
                        break
            else:
                continue
            break
    print("おすすめの企業はこちらです")
    for company in company_list.keys():
        print(company)
    dw.dict_to_json("company.json", company_list)

if __name__ == "__main__":
    main()