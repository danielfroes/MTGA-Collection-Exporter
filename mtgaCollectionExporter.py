import json
import csv
import requests

OUTPUT_PATH = "output/results"

def main():
    cards_owned = get_my_collection_from_mtga()
    mtga_database = get_mtga_database()
    cards_with_full_data = merge_datasets(cards_owned, mtga_database)
    formated_cards = format_cards(cards_with_full_data)
    write_csv(formated_cards, OUTPUT_PATH)


def get_my_collection_from_mtga():
    url = "http://localhost:6842/cards"
    response = request(url)
    return response["cards"]


def get_mtga_database():
    database_path = "database/magicCardsDatabase.json"
    with open(database_path, "r", encoding="utf-8") as database_file:
        database = json.load(database_file)
        return {card["arena_id"] : card for card in database if "arena_id" in card}    
    
def merge_datasets(cards_owned, mtga_database):
    merged = []
    for card in cards_owned:
        id = card["grpId"]
        if(id in mtga_database):
            mtga_database[id].update(card)
            merged.append(mtga_database[id])
    
    return merged


def write_csv(json_data, csv_file):
    with open(csv_file+".csv", 'w', newline='', encoding="utf-8") as csv_file:
        columns = json_data[0].keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        csv_writer.writerows(json_data)



def format_cards(cards):
    return[
        {
            "count": card["owned"],
            "name": card["name"],
            "edition": card["set"],
            "condition": "NM",
            "language": "English",
            "foil": "",
            "collector_number": card["collector_number"]
        }
        for card in cards]


def request(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            print(f"Erro na requisição. Código de status: {response.status_code}")
    except Exception as e:
        print(f"Ocorreu um erro durante a requisição: {e}")

main()