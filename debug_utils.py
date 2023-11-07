import json

def print_dict_as_json(dictionary):
    json_str = json.dumps(dictionary, indent=4)
    print(json_str)

def write_dict_in_file(dictionary):
    json_str = json.dumps(dictionary, indent=4)
    with open("debug.json", "w", encoding="utf-8") as debug_file:
        debug_file.write(json_str)