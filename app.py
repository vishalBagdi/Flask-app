from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

# Read URI from .env
uri = os.getenv("MONGODB_URI")

# Create MongoClient FIRST
client = MongoClient(
    uri,
    server_api=ServerApi('1')
)

# Create database and collection AFTER client
db = client["test"]

collection = db["flask_tutorial"]

# Test connection
try:
    client.admin.command("ping")
    print("MongoDB Connected")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)

    collection.insert_one(form_data)

    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)