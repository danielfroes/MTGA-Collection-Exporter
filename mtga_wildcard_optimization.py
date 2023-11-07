
import os
import re
import json
import debug_utils as debug
from cards_database import *
from mtga_collection import MtgaCollection
 

database = CardsDatabase()
collection = MtgaCollection()

def main():
    decks = get_decks_in_folder()
    cards_to_craft = find_cards_to_craft(decks)
    wildcards = get_wildcards_needed(cards_to_craft)
    debug.print_dict_as_json(cards_to_craft)
    debug.print_dict_as_json(wildcards) 
    
def get_decks_in_folder():
    folder = "decks"
    files = [folder+"/"+f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]   
    return [load_deck(file) for file in files]

def load_deck(file_path):
    main_deck, sideboard = read_deck_file(file_path)
    all_cards = merge_maindeck_and_sideboard(main_deck, sideboard)

    return {
        "name" : file_path.split('/')[-1],
        "main_deck": main_deck,
        "sideboard": sideboard,
        "all_cards": all_cards,
    } 

def merge_maindeck_and_sideboard(maindeck, sideboard):
    all_cards = {}
    for card in maindeck + sideboard :
        name = card["name"]
        if(name in all_cards):
            all_cards[name]["quantity"] += card["quantity"]
        else:
            all_cards[name]= card
    return list(all_cards.values())

def read_deck_file(file_path):
    main_deck = []
    sideboard = []
    section = None
    CARD_LINE_REGEX = r'^(\d+) (.+) \(([^)]+)\) (\d+)(\r\n)?$'

    with open(file_path, 'r', newline='\r\n', encoding="utf-8") as deck_file:
        for line in deck_file:
            line.strip()
            if line.startswith("Deck"):
                section = main_deck
            elif line.startswith("Sideboard"):
                section = sideboard
            elif section is not None and re.match(CARD_LINE_REGEX, line) :
                card = read_card_line(line) 
                section.append(card)

    return main_deck,sideboard      

def read_card_line(line):
    values = line.split()
    card = {
        "quantity" : int(values[0]),
        "name" : " ".join(values[1:-2]),
        "set_code" : values[-2][1:-1],
        "collector_number": values[-1]
    }    
    return card


def find_cards_to_craft(decks):
    merged_decks = decks[0]["all_cards"]
    for deck in decks:
        merged_decks = merge_decks(merged_decks, deck["all_cards"])

    for card in merged_decks:
        card["occurence"] = get_occurence(card, decks)
        card["printings"] = get_printings(card)
        card["missing"] = get_missing_quantity(card)    
        card["lowest_rarity"] = get_lowest_rarity(card)

    return [convert_to_craft(card) for card in merged_decks if card["missing"] > 0]
    
def convert_to_craft(card):
    return {
        "name" : card["name"],
        "occurence" : card["occurence"],
        "missing" : card["missing"],
        "rarity" : card["lowest_rarity"]
    } 

def get_occurence(card, decks):
    count = 0
    for deck in decks:
        count += 1 if card in deck["all_cards"] else 0
    
    return count

def get_printings(card): 
    printings = database.search_cards(lambda data: data["name"].startswith(card["name"]), simplified = True)
    for printing in printings:
        printing_in_collection = collection.get_card(printing["arena_id"])
        printing["owned"] = printing_in_collection["owned"] if printing_in_collection is not None else 0
    
    return printings

def get_missing_quantity(card):
    total_owned = sum(printing["owned"] for printing in card["printings"])

    return max(card["quantity"] - total_owned, 0)

def get_lowest_rarity(card):
    RARITY_ORDER = ["common", "uncommon", "rare", "mythic"]
    lowest_rarity = min(card["printings"], key=lambda x: RARITY_ORDER.index(x["rarity"]))
    return lowest_rarity["rarity"]

def merge_decks(deck_a, deck_b):
    all_cards = {}
    for card in deck_a + deck_b :
        name = card["name"]
        if(name in all_cards):
            all_cards[name]["quantity"] = max(card["quantity"], all_cards[name]["quantity"])
        else:
            all_cards[name] = card
    return list(all_cards.values())



def get_wildcards_needed(cards_to_craft):

    wildcards = {}
    for card in cards_to_craft:
        rarity = card["rarity"]
        if(rarity in wildcards):
            wildcards[rarity] += card["missing"]
        else:
            wildcards[rarity] = card["missing"]

    return wildcards  


main()


#Pegar os que tem cartas para serem craftadas
#Separar todas as cartas a serem craftadas e tirar as repetidas
#com as cartas eu tenho que separar por raridade 
#Printar o resultado
