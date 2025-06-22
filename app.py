from flask import Flask, render_template, request, redirect, url_for
from models import db, Brew

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    brews = Brew.query.order_by(Brew.date.desc()).all()
    return render_template('index.html', brews=brews)

@app.route('/add', methods=['GET', 'POST'])
def add_brew():
    if request.method == 'POST':
        date = request.form['date']
        name = request.form['name']
        roast = request.form['roast']
        method = request.form['method']
        rating = request.form['rating']
        notes = request.form['notes']

        new_brew = Brew(
            date=date,
            name=name,
            roast=roast,
            method=method,
            rating=int(rating),
            notes=notes
        )
        db.session.add(new_brew)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_brew.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = Brew.query

    if request.method == "POST":
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        name = request.form.get('name')
        roast = request.form.get('roast')
        method = request.form.get('method')
        rating_min = request.form.get('rating_min')
        rating_max = request.form.get('rating_max')
        notes = request.form.get('notes')

        if date_from:
            query = query.filter(Brew.date >= date_from)
        if date_to:
            query = query.filter(Brew.date <= date_to)
        if name:
            query = query.filter(Brew.name.ilike(f"%{name}%"))
        if roast and roast != "Any":
            query = query.filter(Brew.roast == roast)
        if method:
            query = query.filter(Brew.method.ilike(f"%{method}%"))
        if rating_min:
            query = query.filter(Brew.rating >= int(rating_min))
        if rating_max:
            query = query.filter(Brew.rating <= int(rating_max))
        if notes:
            query = query.filter(Brew.notes.ilike(f"%{notes}%"))

        results = query.order_by(Brew.date.desc()).all()
        return render_template("search.html", brews=results)
    else:
        return render_template("search.html", brews=[])

if __name__ == '__main__':
    # Proper table creation for Flask 3.x and SQLAlchemy
    with app.app_context():
        db.create_all()
    app.run(debug=True)