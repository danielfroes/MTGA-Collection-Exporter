import json

class CardsDatabase:
    DATABASE_PATH = "database/cardDatabase.json"

    def __init__ (self):
        with open(self.DATABASE_PATH, "r", encoding="utf-8") as database_file:
            raw_database = json.load(database_file)
            self.arena_cards = {card["arena_id"] : card for card in raw_database if "arena_id" in card}

    def search_cards(self, comparison, simplified = False):
        found = list(filter(comparison, self.arena_cards.values()))
        return found if not simplified else [self.simplify(card) for card in found]

    def simplify(self, card):
        return {
            "arena_id": card["arena_id"] if "arena_id" in card else None,
            "name" : card["name"],
            "collector_number" : card["collector_number"],
            "set_code" : card["set"],
            "rarity" : card["rarity"]
        }
