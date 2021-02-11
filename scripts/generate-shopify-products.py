import requests
import csv
from card import Card
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename


Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
print("Select Inventory CSV")
inventory_input_filename = askopenfilename()

print("Importing Cards...")
card_list = []

input_file = open(
    inventory_input_filename,
    "r",
    newline="",
)

csv_reader = csv.DictReader(input_file)

for row in csv_reader:
    new_card = Card()
    new_card.name = row["Card Name"]
    new_card.tag = row["Tag"]
    new_card.box_name = row["Box Name"]
    new_card.rarity = row["Rarity"]
    new_card.price = row["Low"]
    new_card.quantity = row["Quantity"]

    new_card.get_card_data()

    card_list.append(new_card)
    print("Imported " + new_card.name)
    time.sleep(0.5)


output_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/shopify_product_list.csv",
    "w",
    newline="",
)
writer = csv.writer(output_file)
csv_header_row = [
    "Handle",
    "Title",
    "Body (HTML)",
    "Collection",
    "Vendor",
    "Type",
    "Tags",
    "Published",
    "Option1 Name",
    "Option1 Value",
    "Option2 Name",
    "Option2 Value",
    "Option3 Name",
    "Option3 Value",
    "Variant SKU",
    "Variant Grams",
    "Variant Inventory Tracker",
    "Variant Inventory Qty",
    "Variant Inventory Policy",
    "Variant Fulfillment Service",
    "Variant Price",
    "Variant Compare At Price",
    "Variant Requires Shipping",
    "Variant Taxable",
    "Variant Barcode",
    "Image Src",
    "Image Alt Text",
    "Status",
]
writer.writerow(csv_header_row)

for card in card_list:
    card_desc = (
        card.tag + " - " + card.box_name + " - " + card.rarity + "\n" + card.description
    )
    card_row = [
        card.tag,
        card.name,
        card_desc,
        card.box_name,
        "",
        "",
        "",
        "True",
        "Title",
        "Default Title",
        "",
        "",
        "",
        "",
        "",
        0,
        "shopify",
        card.quantity,
        "deny",
        "manual",
        card.price,
        "",
        "TRUE",
        "TRUE",
        "",
        card.img_url,
        card.name,
        "active",
    ]

    writer.writerow(card_row)


input_file.close()
output_file.close()
print("Results Written")
