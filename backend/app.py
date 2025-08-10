from flask import Flask, render_template, request
from flask_mail import Mail
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Load configuration
with open('C:\\Users\\cc\\Documents\\gogu\\our-app\\backend\\config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['mail-user'],
    MAIL_PASSWORD=params['mail-pass']
)
mail = Mail(app)

# Firebase admin initialization
cred = credentials.Certificate("C:\\Users\\cc\\Documents\\gogu\\our-app\\.gitignore\\servicekey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

#timetable class

def Timetable(day,period1,period2,period3,period4,period5,period6,dayOeder):
    return {
        "day":  day,
        "period1": period1,
        "period2": period2,
        "period3": period3,
        "period4": period4,
        "period5": period5,
        "period6": period6,
        "dayOrder": dayOeder
    }

# Contact class
def Contact(name, email, subject, message):
    return {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }

# Homework class
def Homework(subject, details, date):
    return {
        "subject": subject,
        "details": details,
        "date": date
    }

# Routes
@app.route("/")
def home():
    homework_list = []
    try:
        homework_ref = db.collection("homeworks")
        docs = homework_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            hw = Homework(data.get("subject"), data.get("details"), data.get("date"))
            homework_list.append(hw)
    except Exception as e:
        print("Error fetching homework:", e)
    return render_template("index.html", params=params, homework_data=homework_list)

@app.route("/homework", methods=['GET'])
def homework():
    homework_list = []
    try:
        homework_ref = db.collection("homeworks")
        docs = homework_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            hw = Homework(data.get("subject"), data.get("details"), data.get("date"))
            homework_list.append(hw)
    except Exception as e:
        print("Error fetching homework:", e)

    return render_template("homework.html", homework_data=homework_list, params=params)

@app.route("/timetable")
def timetable():
     timetable_list = []
     try:
        timetable_ref = db.collection("timetable").order_by("dayOrder")
        docs = timetable_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            tt = Timetable(
                data.get("day"),
                data.get("period1"),
                data.get("period2"),
                data.get("period3"),
                data.get("period4"),
                data.get("period5"),
                data.get("period6"),
                data.get("dayOrder")
            )
            timetable_list.append(tt)
     except Exception as e:
        print("Error fetching timetable:", e)

     return render_template("timetable.html", params=params,timetable=timetable_list)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        db.collection("contact").add(Contact(name, email, subject, message))

        mail.send_message(
            'Homework App Query from ' + name,
            sender=email,
            recipients=[params['mail-user']],
            body=subject + "\n\n" + message + "\n\nfrom: " + email + "\n\nThank you"
        )

    return render_template("contact.html", success=True, params=params)

@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html", params=params)

@app.route("/upload")
def upload():
    return render_template("upload.html", params=params)

if __name__ == "__main__":
    app.run(debug=True) 
