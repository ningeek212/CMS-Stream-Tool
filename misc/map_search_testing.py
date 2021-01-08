from json import load, dump

with open("maps.json") as file:
    map_dict = load(file)

while True:
    query = input("Map Name: ")
    for item in map_dict:
        if query.lower() in item["name"].lower():
            print(item["name"])