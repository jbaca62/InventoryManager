import requests


class Location:
    def __init__(self, location_name=None, t=None):
        if location_name != None:
            self.id = 0
            self.name = location_name
            self.cardId = ""
        if t != None:
            self.id = t[0]
            self.name = t[1]
            self.cardId = t[2]

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["cardId"] = self.cardId
        return d
