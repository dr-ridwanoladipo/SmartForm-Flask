# Import necessary modules
from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure application settings
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

# Initialize database
db = SQLAlchemy(app)

# Initialize mail
mail = Mail(app)


# Define Form model
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


# Define route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        # Create and save new form entry
        form = Form(first_name=first_name, last_name=last_name, email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        # Prepare and send email
        message_body = (f"Thank you for your submission, {first_name}. Here are your data: "
                        f"{first_name}\n{last_name}\n{date}.\nThank you")
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        # Flash success message
        flash(f"{first_name}, Your form was submitted successfully!", "success")

    return render_template("index.html")


# Run the application
if __name__ == "__main__":
    with app.app_context():
        # Create database tables
        db.create_all()
        # Run the Flask app in debug mode
        app.run(debug=True, port=5001)