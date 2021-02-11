import requests
import csv


temp_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/scripts/price_list-intermediate.csv",
    "w",
    newline="",
)
writer = csv.writer(temp_file)
writer.writerow(["Card Name", "Tag", "Box Name", "Rarity", "High", "Average", "Low"])

quantity = {}

while True:

    card_tag = str(input("Card Tag: "))
    card_tag = card_tag.upper()
    if card_tag == "DONE":
        break

    if card_tag in quantity.keys():
        quantity[card_tag] = quantity[card_tag] + 1
        print(card_tag, ": ", quantity[card_tag])
        continue

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

        quantity[card_tag] = 1

        print(card_name, ": ", card_high, card_avg, card_low)

        row = [
            card_name,
            card_tag,
            box_name,
            card_rarity,
            card_high,
            card_avg,
            card_low,
        ]
        writer.writerow(row)
    else:
        print("Invalid Response. Re-enter tag.")


temp_file.close()

print("Writing Results...")

write_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/scripts/inventory_list.csv",
    "w",
    newline="",
)
writer = csv.writer(write_file)
writer.writerow(
    ["Card Name", "Tag", "Quantity", "Box Name", "Rarity", "High", "Average", "Low"]
)

read_file = open(
    "/Users/jacob/Documents/Online Trading Card Store/scripts/price_list-intermediate.csv",
    "r",
    newline="",
)
reader = csv.DictReader(read_file)

for row in reader:
    buffer = [
        row["Card Name"],
        row["Tag"],
        quantity[row["Tag"]],
        row["Box Name"],
        row["Rarity"],
        row["High"],
        row["Average"],
        row["Low"],
    ]
    writer.writerow(buffer)

read_file.close()
write_file.close()

print("Results Written")
