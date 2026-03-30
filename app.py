from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, Event

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create DB Tables
with app.app_context():
    db.create_all()

# Dashboard
@app.route("/")
def dashboard():
    total_events = Event.query.count()
    return render_template("dashboard.html", total_events=total_events)

# View Events
@app.route("/events")
def events():
    all_events = Event.query.all()
    return render_template("events.html", events=all_events)

# Add Event
@app.route("/add", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        description = request.form["description"]

        new_event = Event(name=name, date=date, location=location, description=description)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("events"))

    return render_template("add_event.html")

# Edit Event
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_event(id):
    event = Event.query.get_or_404(id)

    if request.method == "POST":
        event.name = request.form["name"]
        event.date = request.form["date"]
        event.location = request.form["location"]
        event.description = request.form["description"]

        db.session.commit()
        return redirect(url_for("events"))

    return render_template("edit_event.html", event=event)

# Delete Event
@app.route("/delete/<int:id>")
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("events"))

if __name__ == "__main__":
    app.run(debug=True)