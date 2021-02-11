import DBInterface as DB
import requests
from card import Card

DB.get_all_cards()

while True:

    card_tag = str(input("Card Tag: "))
    card_tag = card_tag.upper()
    if card_tag == "DONE":
        break

    if DB.does_card_exists(card_tag):
        # Is in Database
        updated_quantity = DB.increment_card_quantity(card_tag)
        print(updated_quantity)
    else:
        # Not in Database
        new_card = Card(card_tag)
        new_card.get_card_data()
        DB.add_card(new_card)
        print(
            new_card.name, new_card.price_high, new_card.price_avg, new_card.price_low
        )
