from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from tagfilter import Filter


app = Flask(__name__)

file_path = os.path.abspath(os.getcwd()) + "/blog.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    post.content = Filter.filter_tags(post.content)
    return render_template('post.html', post=post)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('edit.html', post=post)


@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
def editpost(post_id):
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    filtered_content = Filter.filter_tags(content)

    post = Blogpost.query.get(post_id)
    post.title = title
    post.subtitle = subtitle
    post.author = author
    post.content = filtered_content

    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    Blogpost.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
