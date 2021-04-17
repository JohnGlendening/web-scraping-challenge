from flask import Flask, redirect, render_template
from pymongo import MongoClient
import scrape_mars

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client.mars

db.mars_df.drop()


@app.route('/')
def home():
    data = db.mars_df.find_one()

    return render_template('index.html', data=data)


@app.route('/scrape')
def mars_scrape():
    db.mars_df.drop()
    data_scrape = scrape_mars.scrape()
    db.mars_df.update({}, data_scrape, upsert=True)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
