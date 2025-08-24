from flask import Flask, render_template, request
from flask_mail import Mail
import firebase_admin
from firebase_admin import credentials, firestore
import json, os

# Load params from environment variable (paste config.json contents into APP_CONFIG env var)
params = json.loads(os.environ.get("APP_CONFIG", "{}"))

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params.get('mail-user'),
    MAIL_PASSWORD=params.get('mail-pass')
)
mail = Mail(app)

# Firebase Admin initialization using env var FIREBASE_SERVICE_KEY
service_account_json = os.environ.get("FIREBASE_SERVICE_KEY")
if service_account_json:
    try:
        cred = credentials.Certificate(json.loads(service_account_json))
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        print("Firebase initialization error:", e)
        db = None
else:
    db = None


# ---------- Helper functions ----------
def Timetable(day, period1, period2, period3, period4, period5, period6, period7, period8, dayOrder):
    return {
        "day": day,
        "period1": period1,
        "period2": period2,
        "period3": period3,
        "period4": period4,
        "period5": period5,
        "period6": period6,
        "period7": period7,
        "period8": period8,
        "dayOrder": dayOrder
    }

def Contact(name, email, subject, message):
    return {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }

def Homework(subject, details, date, file_url=None):
    return {
        "subject": subject,
        "details": details,
        "date": date,
        "file_url": file_url
    }


# ---------- Routes ----------
@app.route("/")
def home():
    homework_list = []
    if db:
        try:
            docs = db.collection("homeworks").stream()
            for doc in docs:
                data = doc.to_dict()
                homework_list.append(Homework(
                    data.get("subject"),
                    data.get("details"),
                    data.get("date"),
                    data.get("file_url")
                ))
        except Exception as e:
            print("Error fetching homework:", e)

    return render_template("index.html", params=params, homework_data=homework_list)


@app.route("/homework")
def homework():
    homework_list, subjects = [], []
    if db:
        try:
            docs = db.collection("homeworks").stream()
            for doc in docs:
                data = doc.to_dict()
                hw = Homework(
                    data.get("subject"),
                    data.get("details"),
                    data.get("date"),
                    data.get("file_url")
                )
                homework_list.append(hw)

            # Build unique subjects list, max 6
            seen = set()
            for hw in homework_list:
                if hw['subject'] and hw['subject'] not in seen:
                    subjects.append(hw['subject'])
                    seen.add(hw['subject'])
                if len(subjects) >= 6:
                    break
        except Exception as e:
            print("Error fetching homework:", e)

    return render_template("homework.html", homework_data=homework_list, subjects=subjects, params=params)


@app.route("/timetable")
def timetable():
    timetable_list = []
    if db:
        try:
            docs = db.collection("timetable").order_by("dayOrder").stream()
            for doc in docs:
                data = doc.to_dict()
                timetable_list.append(Timetable(
                    data.get("day"),
                    data.get("period1"),
                    data.get("period2"),
                    data.get("period3"),
                    data.get("period4"),
                    data.get("period5"),
                    data.get("period6"),
                    data.get("period7"),
                    data.get("period8"),
                    data.get("dayOrder")
                ))
        except Exception as e:
            print("Error fetching timetable:", e)

    return render_template("timetable.html", params=params, timetable=timetable_list)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST' and db:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        try:
            db.collection("contact").add(Contact(name, email, subject, message))
            mail.send_message(
                'Homework App Query from ' + name,
                sender=email,
                recipients=[params.get('mail-user')],
                body=subject + "\n\n" + message + "\n\nfrom: " + email + "\n\nThank you"
            )
        except Exception as e:
            print("Error saving contact or sending mail:", e)

    return render_template("contact.html", success=True, params=params)


@app.route("/syllabus")
def syllabus():
    return render_template("syllabus.html", params=params)


@app.route("/upload")
def upload():
    return render_template("upload.html", params=params)


# ---------- Run ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port)
