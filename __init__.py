from flask import Flask, render_template, request, jsonify
import sys
from flask_cors import CORS
import DBInterface as DB
from card import Card

app = Flask(__name__)
CORS(app)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/cards")
def cards():
    cards = DB.get_all_cards()
    return render_template("cards.html", cards=cards)


@app.route("/cards/add", methods=["GET", "POST"])
def add_card():
    if request.method == "GET":
        return render_template("add_card.html")
    if request.method == "POST":
        cardTag = request.form["cardTag"].upper()
        card = Card(cardTag)
        card.get_card_data()
        db_card = DB.add_card(card)
        return jsonify(db_card.to_dict())


@app.route("/locations")
def locations():
    locations = DB.get_all_locations()
    return render_template("locations.html", locations=locations)


@app.route("/locations/add", methods=["GET", "POST"])
def add_location():
    if request.method == "GET":
        return render_template("add_location.html")
    if request.method == "POST":
        cardTag = request.form["cardTag"].upper()
        card = Card(cardTag)
        card.get_card_data()
        db_card = DB.add_card(card)
        return jsonify(db_card.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0")
