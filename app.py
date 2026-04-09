from flask import Flask, render_template, request, redirect, url_for , session
from sqlalchemy import or_
from config import Config
from models import db, Event ,User
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()




@app.route("/events")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 5 ))
    search = request.args.get("search", "")

    query = Event.query

    
    if search:
        query = query.filter(
            or_(
                Event.id.like(f"%{search}%"),
                Event.name.ilike(f"%{search}%"),
                Event.date.like(f"%{search}%"),
                Event.location.ilike(f"%{search}%")
            )
        )

    total = query.count()

    offset = (page - 1) * size

    events = query.limit(size).offset(offset).all()

    return render_template(
        "events.html",
        events=events,
        page=page,
        size=size,
        total=total,
        search=search
    )


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # password hash
        hashed_password = generate_password_hash(password)

        user = User(email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")




@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        
        user = User.query.filter_by(email=email).first()

        
        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            return redirect(url_for("index"))

        else:
            return "Invalid Email or Password"

    return render_template("login.html")
# Add Event
@app.route("/add", methods=["GET", "POST"])
def add_event():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"]
        date = request.form["date"]
        location = request.form["location"]
        description = request.form["description"]

        new_event = Event(
            name=name,
            date=date,
            location=location,
            description=description
        )

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("index"))

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

        return redirect(url_for("index"))

    return render_template("edit_event.html", event=event)


# Delete Event
@app.route("/delete/<int:id>")
def delete_event(id):

    event = Event.query.get_or_404(id)

    db.session.delete(event)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)