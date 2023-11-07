import json
import csv
import debug_utils as debug
from cards_database import *
from mtga_collection import MtgaCollection

database = CardsDatabase()
collection = MtgaCollection()

OUTPUT_PATH = "output/results"

def main():
    cards_with_full_data = merge_datasets(collection.cards_owned, database.arena_cards)
    debug.write_dict_in_file(cards_with_full_data)
    formated_cards = format_cards(cards_with_full_data)
    write_csv(formated_cards, OUTPUT_PATH)


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
            "collector_number": card["collector_number"]
        }
        for card in cards]



main()