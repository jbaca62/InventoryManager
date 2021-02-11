"""
Generates 2 files: new_products.csv and updated_inventory.csv
new_products.csv contains all new products, with their starting inventory
updated_inventory.csv contains the updated quantities for all existing items

New Products will not be included in the updated inventory list and vice versa.

Input Files: inventory list csv from shopify
"""

import csv
import requests
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

from card import Card

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
print("Select Inventory CSV")
inventory_input_filename = (
    askopenfilename()
)  # show an "Open" dialog box and return the path to the selected file

print("Importing Quantity Data From ", inventory_input_filename)

inventory_input_file = open(
    inventory_input_filename,
    "r",
    newline="",
)

csv_reader = csv.DictReader(inventory_input_file)

existing_quantity = {}
for row in csv_reader:
    existing_quantity[row["Handle"].upper()] = int(row["PO Box 273"])

inventory_input_file.close()

print("Existing Quantity Calculated")

print("Enter cards to add to inventory: ")

new_card_list = []

new_card_quantity = {}

while True:

    card_tag = str(input("Card Tag: "))
    card_tag = card_tag.upper()
    if card_tag == "DONE":
        break

    ## Previously listed on shopify
    if card_tag in existing_quantity.keys():
        existing_quantity[card_tag] = existing_quantity[card_tag] + 1
        print(card_tag, ": ", existing_quantity[card_tag])
        continue

    ## Not previously listed on shopify but enter in this session
    if card_tag in new_card_quantity.keys():
        new_card_quantity[card_tag] = new_card_quantity[card_tag] + 1
        print(card_tag, ": ", new_card_quantity[card_tag])
        continue

    ## Must Be New Card
    response = requests.get(
        "http://yugiohprices.com/api/price_for_print_tag/" + card_tag
    )

    if response.status_code == 200:
        response_body = response.json()
        if response_body["status"] == "fail":
            print("Failed Response. Re-enter tag.")
            continue
        data = response_body["data"]
        card_name = data["name"]
        price_data = data["price_data"]

        box_name = price_data["name"]
        card_tag = price_data["print_tag"]
        card_rarity = price_data["rarity"]

        prices = price_data["price_data"]["data"]["prices"]
        card_high = prices["high"]
        card_low = prices["low"]
        card_avg = prices["average"]

        new_card_quantity[card_tag] = 1

        print(card_name, ": ", card_high, card_avg, card_low)

        new_card = Card()
        new_card.name = card_name
        new_card.tag = card_tag
        new_card.box_name = box_name
        new_card.rarity = card_rarity
        new_card.price = card_low
        new_card.get_card_data()

        new_card_list.append(new_card)

    else:
        print("Invalid Response. Re-enter tag.")

inventory_input_file = open(inventory_input_filename, "r", newline="")
csv_reader = csv.DictReader(inventory_input_file)

inventory_output_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/updated_inventory_list.csv",
    "w",
    newline="",
)
writer = csv.writer(inventory_output_file)

inventory_header_row = [
    "Handle",
    "Title",
    "Option1 Name",
    "Option1 Value",
    "Option2 Name",
    "Option2 Value",
    "Option3 Name",
    "Option3 Value",
    "SKU",
    "HS Code",
    "COO",
    "PO Box 273",
]
writer.writerow(inventory_header_row)

for row in csv_reader:
    tag = row["Handle"].upper()
    new_row = [
        row["Handle"],
        row["Title"],
        row["Option1 Name"],
        row["Option1 Value"],
        row["Option2 Name"],
        row["Option2 Value"],
        row["Option3 Name"],
        row["Option3 Value"],
        row["SKU"],
        row["HS Code"],
        row["COO"],
        existing_quantity[tag],
    ]
    writer.writerow(new_row)

inventory_input_file.close()
inventory_output_file.close()

new_products_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/new_product_list.csv",
    "w",
    newline="",
)
writer = csv.writer(new_products_file)
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

for card in new_card_list:
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
        new_card_quantity[card.tag],
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


print("Files Written")

"""
quantity = {}
    card_tag = row["Handle"].upper()
    if card_tag in quantity.keys():
        quantity[card_tag] = quantity[card_tag] + 1
        print(card_tag, ": ", quantity[card_tag])
        continue
"""
