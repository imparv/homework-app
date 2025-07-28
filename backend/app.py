from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials , firestore

app= Flask(__name__)

#firebase admin 
cred = credentials.Certificate("C:\\Users\\cc\\Documents\\gogu\\our-app\\.gitignore\\servicekey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/homework.html")
def homework():
    return render_template("homework.html")
@app.route("/timetable.html")
def timetable():
    return render_template("timetable.html")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")
@app.route("/syllabus.html")
def syllabus():
    return render_template("syllabus.html")
@app.route("/upload.html")
def upload():
    return render_template("upload.html")





if __name__ == "__main__":
    app.run(debug=True)