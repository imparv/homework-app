from flask import Flask, render_template,request
import firebase_admin
from firebase_admin import credentials , firestore
import json


with open('C:\\Users\\cc\\Documents\\gogu\\our-app\\backend\\config.json','r') as c:
    params = json.load(c)["params"]

app= Flask(__name__)

#firebase admin 
cred = credentials.Certificate("C:\\Users\\cc\\Documents\\gogu\\our-app\\.gitignore\\servicekey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# contact class to submit the form to firebase
class Contact:
    def __init__(self,name,email,subject,message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message 
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message
        }
# routes start

# homepage
@app.route("/")
def home():
    return render_template("index.html")
 
 # homework page
@app.route("/homework")
def homework():
    return render_template("homework.html")

#timetable page
@app.route("/timetable")
def timetable():
    return render_template("timetable.html")

#contact
@app.route("/contact",methods = ['GET','POST'])
def contact():
    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        #define entry to send to fire base
        new_contact = Contact(name, email, subject, message)
        db.collection("contact").add(new_contact.to_dict())  

    return render_template("contact.html",success=True) 

# syllabus page
@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html")

# upload page
@app.route("/upload")
def upload():
    return render_template("upload.html")




if __name__ == "__main__":
    app.run(debug=True)