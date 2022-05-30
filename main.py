from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FlaskApp.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/guest-book')
def guest_book():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('guest-book.html', articles=articles)


@app.route('/guest-book/<int:id>')
def message_detail(id):
    article = Article.query.get(id)
    return render_template('message-detail.html', article=article)


@app.route('/guest-book/<int:id>/delete', methods=['POST', 'GET'])
def message_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()

        return redirect('/guest-book')
    except:
        article = Article.query.get(id)
        return render_template('message-update.html', article=article)


@app.route('/guest-book/<int:id>/update', methods=['POST', 'GET'])
def update_message(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()

            return redirect('/guest-book')
        except:
            return "An error occurred when updating article, please try again. "
    else:
        return render_template('message-update.html', article=article)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()

            return redirect('/guest-book')
        except:
            return "An error occurred when adding article, please try again. "
    else:
        return render_template('login.html')


@app.route('/about')
def about():
    return app.send_static_file('about.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/gallery-2')
def gallery_2():
    return render_template('gallery-2.html')


if __name__ == "__main__":
    app.run(debug=False)
