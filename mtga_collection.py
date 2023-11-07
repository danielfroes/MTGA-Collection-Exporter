
import requests
import json

class MtgaCollection:
    URL = "http://localhost:6842/cards"

    def __init__(self):
        response = request(self.URL)
        self.cards_owned = response["cards"]
        self.cards_by_arenaId = {card["grpId"] : card for card in self.cards_owned}

    
    def get_card(self, arenaId):
        if(arenaId in self.cards_by_arenaId):
            return self.cards_by_arenaId[arenaId]


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
