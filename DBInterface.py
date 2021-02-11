import pyodbc

from card import Card
from location import Location

from config import DB_INFO

SQL_GET_ALL_ROWS_FROM_TABLE = "SELECT * FROM Cards;"
SQL_ADD_CARD = "INSERT INTO Cards([CardName],[CardTag],[Box],[Rarity],[PriceHigh],[PriceAvg],[PriceLow],[Quantity],[Location],[Description],[Listings]) VALUES ( ?, ?, ?,?,?, ?,?,?,?,?,?)"
SQL_GET_CARD_QUANTITY_BY_CARDTAG = "SELECT [Quantity] FROM Cards WHERE CardTag = ?"
SQL_UPDATE_CARD_QUANTITY_BY_CARDTAG = "UPDATE Cards SET Quantity = ? WHERE CardTag = ?"
SQL_CHECK_IF_CARD_EXISTS_FROM_TAG = "SELECT 1 FROM Cards WHERE CardTag = ?;"
SQL_GET_CARD_FROM_TAG = "SELECT * FROM Cards WHERE CardTag = ?;"
SQL_GET_ALL_LOCATIONS = "SELECT * FROM Locations;"


def generate_connection(info):
    return pyodbc.connect(
        "DRIVER="
        + info["driver"]
        + ";SERVER="
        + info["server"]
        + ";PORT=1433;DATABASE="
        + info["database"]
        + ";UID="
        + info["username"]
        + ";PWD="
        + info["password"]
    )


# Card Stuff


def get_all_cards():
    db_conn = generate_connection(DB_INFO)
    cursor = db_conn.cursor()
    cursor.execute(SQL_GET_ALL_ROWS_FROM_TABLE)
    rows = cursor.fetchall()
    card_list = []
    for row in rows:
        card = Card(t=row)
        card_list.append(card)
    db_conn.close()
    return card_list


def get_card(card_tag):
    if does_card_exist(card_tag):
        db_conn = generate_connection(DB_INFO)
        cursor = db_conn.cursor()
        cursor.execute(SQL_GET_CARD_FROM_TAG, card_tag)
        row = cursor.fetchone()
        print(row)
        db_conn.close()
        return Card(t=row)
    else:
        return None


def add_card(card):
    card_exists = does_card_exist(card.tag)
    if card_exists:
        increment_card_quantity(card.tag)
        return get_card(card.tag)
    else:
        card_data = (
            card.name,
            card.tag,
            card.box_name,
            card.rarity,
            card.price_high,
            card.price_avg,
            card.price_low,
            1,
            "None",
            card.description,
            "None",
        )

        db_conn = generate_connection(DB_INFO)
        cursor = db_conn.cursor()
        cursor.execute(SQL_ADD_CARD, card_data)
        cursor.commit()
        db_conn.close()
        return get_card(card.tag)


def get_card_quantity(card_tag):
    db_conn = generate_connection(DB_INFO)
    cursor = db_conn.cursor()
    cursor.execute(SQL_GET_CARD_QUANTITY_BY_CARDTAG, card_tag)
    row = cursor.fetchone()
    quantity = row[0]
    db_conn.close()
    return quantity


def update_card_quantity(card_tag, new_quantity):
    db_conn = generate_connection(DB_INFO)
    cursor = db_conn.cursor()
    cursor.execute(SQL_UPDATE_CARD_QUANTITY_BY_CARDTAG, (new_quantity, card_tag))
    cursor.commit()
    db_conn.close()


def does_card_exist(card_tag):
    db_conn = generate_connection(DB_INFO)
    cursor = db_conn.cursor()
    cursor.execute(SQL_CHECK_IF_CARD_EXISTS_FROM_TAG, card_tag)
    row = cursor.fetchone()
    db_conn.close()
    if row == None:
        return False
    else:
        return True


def increment_card_quantity(card_tag):
    current_quantity = get_card_quantity(card_tag)
    update_card_quantity(card_tag, current_quantity + 1)
    return get_card_quantity(card_tag)


# Location Stuff


def get_all_locations():
    db_conn = generate_connection(DB_INFO)
    cursor = db_conn.cursor()
    cursor.execute(SQL_GET_ALL_LOCATIONS)
    rows = cursor.fetchall()
    location_list = []
    for row in rows:
        loc = Location(t=row)
        location_list.append(loc)
    db_conn.close()
    return location_list