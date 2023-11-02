from flask import Flask, render_template, request, redirect
from sqlalchemy import and_
import os
from werkzeug.utils import secure_filename
from models import db
from models import *

from dotenv import load_dotenv

load_dotenv()


user = 'root'
password = ''
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlitedb.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@localhost/flaskblogdb'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MEDIUM_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@localhost/flaskblogdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD'] = os.path.join('static', 'uploads')

app.app_context().push()

db.init_app(app)



# *************** Routes *****************

@app.route('/')
def home():
    if request.args.get('search'):
        print('We have search: ', request.args.get('search'))
        posts = Post.query.filter(Post.post_title.contains(request.args['search'])).all()
    else:
        posts = Post.query.all()
    return render_template('index.html', posts = posts)


@app.route('/post/<int:postid>/<string:title>/')
def post_detail(postid, title):
    post = Post.query.filter_by(id=postid, post_title = title).first()
    related_posts = Post.query.filter_by(category = post.category).all()
    return render_template('post.html', post = post, related_posts = related_posts)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        searchedword = request.form.get('search')
        return redirect(f'/?search={searchedword}')
    return redirect('/')


@app.route('/author/<int:id>', methods=['GET'])
def author(id):
    author = Author.query.get(id)
    posts_from_author = Post.query.filter_by(author = id).all()
    return render_template('author.html', author=author, posts_from_author = posts_from_author)


@app.route('/new-post/', methods=['GET', 'POST'])
def add_new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        category = request.form.get('category')
        image = request.files['image']

        filename= secure_filename(image.filename)

        fname= os.path.join(app.config['UPLOAD'] , secure_filename(filename))
        
        image.save(fname)
        db.session.add(Post(post_title = title, post_body= content, cover = fname, author = author, category = int(category), slug= title) )
        db.session.commit()
        print('New Post saved to DB.')

        return redirect('/')

    else:
        return render_template('newpost.html', post=None)


@app.route('/post/edit/<int:id>/<string:title>/', methods=['GET', 'POST'])
def edit_post(id, title):
    post = Post.query.filter_by(id = id, post_title = title).first()

    if request.method == 'POST':
        imagefileuploaded= request.files.get('image')

        post.post_title = request.form.get('title')
        post.author = request.form.get('author')
        post.post_body = request.form.get('content')
        post.category = request.form.get('category')
        post.slug = request.form.get('title')

        if imagefileuploaded:
            filename= secure_filename(imagefileuploaded.filename)
            fname= os.path.join(app.config['UPLOAD'] , secure_filename(filename))
            post.cover = fname
            imagefileuploaded.save(fname)

        db.session.commit()
      
        return redirect('/')

    else:
        return render_template('newpost.html', post=post)



if __name__ == '__main__':
    app.run(debug= True)