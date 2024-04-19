from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

app = Flask(__name__)
CORS(app)

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

predictions = model.predict(x_test)
report = classification_report(y_test, predictions)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    print("------------REQUEST ", request.json)
    user_input = request.json
    if user_input == None:
        return jsonify("missing user input")
    prediction = model.predict([user_input])[0]
    return jsonify(prediction)

@app.route("/")
def get_classification_report():
    return jsonify(report)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

