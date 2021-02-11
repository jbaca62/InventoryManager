import requests


class Card:
    def __init__(self, card_tag=None, t=None):
        if card_tag != None:
            self.id = 0
            self.name = ""
            self.description = ""
            self.tag = card_tag
            self.box_name = ""
            self.rarity = ""
            self.price_low = ""
            self.price_avg = ""
            self.price_high = ""
            self.img_url = ""
            self.quantity = ""
            self.location = ""
        if t != None:
            self.id = t[0]
            self.name = t[1]
            self.tag = t[2]
            self.box_name = t[3]
            self.rarity = t[4]
            self.price_low = float(t[5])
            self.price_avg = float(t[6])
            self.price_high = float(t[7])
            self.quantity = t[8]
            self.location = t[9]
            self.description = t[10]
            self.listing = t[11]
            self.img_url = ""

    """
    def __init__(self, t):
        self.id = t[0]
        self.name = t[1]
        self.tag = t[2]
        self.box_name = t[3]
        self.rarity = t[4]
        self.price_low = t[5]
        self.price_avg = t[6]
        self.price_high = t[7]
        self.quantity = t[8]
        self.location = t[9]
        self.description = t[10]
        self.listing = t[11]
    """

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["description"] = self.description
        d["tag"] = self.tag
        d["box name"] = self.box_name
        d["rarity"] = self.rarity
        d["price low"] = self.price_low
        d["price avg"] = self.price_avg
        d["price high"] = self.price_high
        d["img url"] = self.img_url
        d["quantity"] = self.quantity
        d["location"] = self.location
        return d

    def get_card_data(self):
        response = requests.get(
            "http://yugiohprices.com/api/price_for_print_tag/" + self.tag
        )

        if response.status_code == 200:
            response_body = response.json()
            if response_body["status"] == "fail":
                print("Failed Response. Re-enter tag.")
            else:
                data = response_body["data"]
                self.name = data["name"]
                price_data = data["price_data"]

                self.box_name = price_data["name"]
                self.tag = price_data["print_tag"]
                self.rarity = price_data["rarity"]

                prices = price_data["price_data"]["data"]["prices"]
                self.price_high = prices["high"]
                self.price_low = prices["low"]
                self.price_avg = prices["average"]

                response = requests.get(
                    "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=" + self.name
                )

                if response.status_code == 200:
                    response_body = response.json()
                    data = response_body["data"][0]
                    self.description = data["desc"]
                    self.img_url = data["card_images"][0]["image_url"]

        else:
            print("Invalid Response. Re-enter tag.")
