import json
import sys
import re


def json_to_dict(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data

def dict_to_json(file_name, dict_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(dict_name, f, ensure_ascii=False, indent=4)

def update_json(file_name, appendex_dict):
    json_data = json_to_dict(file_name)
    json_data.update(appendex_dict)
    dict_to_json(file_name, json_data)

def main():
    args = sys.argv
    file_name = "parameters/" + args[1] + ".json"
    param = json_to_dict(file_name)
    a = []
    for key in param.keys():
        if re.search(args[2], key):
            a.append(key)
    if len(a) == 0:
        return
    value = param[a[0]]
    appendex_dict = {}
    appendex_dict[args[1]] = value
    update_json("wish.json", appendex_dict)

if __name__ == "__main__":
    main()