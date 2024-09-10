from flask import Flask, render_template, request

# Initialize Flask application
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        occupation = request.form["occupation"]

    return render_template("index.html")


if __name__ == "__main__":

    # Run the Flask app
    app.run(debug=True, port=5001)