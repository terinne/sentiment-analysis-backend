from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")
jwt = JWTManager(app)

# read the data and clean it
df_train = pd.read_csv("train.csv", encoding='unicode_escape')
df_test = pd.read_csv("test.csv", encoding='latin1')

df_train.drop(columns={'textID', 'selected_text', 'Time of Tweet', 'Age of User', 'Country', 'Population -2020', 'Land Area (Km²)', 'Density (P/Km²)'}, inplace=True)
df_train.dropna(inplace=True)

df_test.drop(columns={'textID', 'Time of Tweet', 'Age of User', 'Country', 'Population -2020', 'Land Area (Km²)', 'Density (P/Km²)'}, inplace=True)
df_test.dropna(inplace=True)

x_train = df_train['text']
x_test = df_test['text']
y_train = df_train['sentiment']
y_test = df_test['sentiment']

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LinearSVC())
])

model.fit(x_train, y_train)
print('the model has been trained')

username_env = os.getenv("USER_NAME")
password_env = os.getenv("PASSWORD")

@app.route("/predict", methods=["GET", "POST"])
@jwt_required()
def predict():
    # print("------------REQUEST ", request.json)
    user_input = request.json
    if user_input == None:
        return jsonify("missing user input")
    prediction = model.predict([user_input])[0]
    return jsonify(prediction)

@app.route("/login", methods=["GET", "POST"])
def create_token():
    username_req = request.json.get("username", None)
    password_req = request.json.get("password", None)

    if username_req == username_env and password_req == password_env:
        access_token = create_access_token(identity=username_env)
        return jsonify({ "token": access_token, "username": username_env })
    else:
        return jsonify('Login failed'), 401

@app.route("/")
def home():
    return "<p> GET /</p"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

