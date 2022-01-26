from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url)[0]
    tables.columns=["Description","Mars","Earth"]
    tables.set_index("Description", inplace=True)
    stats = tables.to_html()
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars,stats =stats)


@app.route("/scrape")
def scraper():
    # mars = mongo.db.mars
    mars_dict = scrape_mars.scrape()
    mongo.db.mars.update_one({},{"$set":mars_dict}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
