# Import Dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Setup Flask App
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()