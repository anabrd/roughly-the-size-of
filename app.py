import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from datetime import timedelta

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

app = Flask(__name__)

# Initialize SQLite for info database
db = SQL("sqlite:///info.db")
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/compare", methods=["GET", "POST"])
def compare():

    if request.method == "POST":

        # Accessing country value from the compare form

        country_name = request.form.get("country")

        # Accessing parameter value from the compare form

        parameter = request.form.get("parameter")

        # Accessing databate and querying for relevant information based on user input

        if parameter == "size":

            country_value = db.execute("SELECT size FROM countries WHERE name = ?", country_name)

            country_size = country_value[0]["size"]

            state_sizes = db.execute("SELECT size FROM states")

            data = []

            for item in state_sizes:
                data.append(item["size"])


            result = data[min(range(len(data)), key = lambda i: abs(data[i]-country_size))]

            state_info = db.execute("SELECT * FROM states WHERE size = ?", result)
            state_size = state_info[0]["size"]

            state_name = state_info[0]["name"]
            ratio = round(country_size/state_size)

            # Update the seach history list

            if "results" not in session:
                session["results"] = []

            session["results"].append({"country": country_name, "ratio": ratio, "state": state_name, "parameter": parameter})

            return render_template("resultsize.html", country_name=country_name, state_name=state_name, ratio=ratio)


        else:

            country_value = db.execute("SELECT population FROM countries WHERE name = ?", country_name)
            country_pop = country_value[0]["population"]

            state_pops = db.execute("SELECT population FROM states")

            data = []

            for state_pop in state_pops:
                data.append(state_pop["population"])


            result = data[min(range(len(data)), key = lambda i: abs(data[i]-country_pop))]

            state_info = db.execute("SELECT * FROM states WHERE population = ?", result)

            state_pop = state_info[0]["population"]

            state_name = state_info[0]["name"]

            ratio = round(country_pop/state_pop)


# Update the seach history list

            if "results" not in session:
                session["results"] = []

            # Accounting for states with population smaller than any state

            if country_pop < 400000:
                state_name = "None"
                ratio = 0

            session["results"].append({"country": country_name, "ratio": ratio, "state": state_name, "parameter": parameter})

            return render_template("resultpop.html", country_name=country_name, state_name=state_name, ratio=ratio, country_pop=country_pop)

    else:
        names = db.execute("SELECT name FROM countries ORDER BY name ASC")
        return render_template("compare.html", names=names)


@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/searches")
def searches():

    return render_template("searches.html", results = session["results"])