from flask import Flask, render_template,request
import firebase_admin
from firebase_admin import credentials , firestore

app= Flask(__name__)

#firebase admin 
cred = credentials.Certificate("C:\\Users\\cc\\Documents\\gogu\\our-app\\.gitignore\\servicekey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()
class contact:
    def __init__(self,name,email,subject,message):
        self.name = name
        self.email = email
        self.subject = message
        self.message = message 
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message
        }

    







@app.route("/")
def home():
    return render_template("index.html")

@app.route("/homework")
def homework():
    return render_template("homework.html")

@app.route("/timetable")
def timetable():
    return render_template("timetable.html")

@app.route("/contact",method = ['GET','POST'])
def contact():
    if(request.method==['POST']):
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()







    return render_template("contact.html")

@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")






if __name__ == "__main__":
    app.run(debug=True)