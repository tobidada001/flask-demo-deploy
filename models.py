from sqlalchemy import Identity, ForeignKey, Boolean
from datetime import datetime
# from app import app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Categories(db.Model):
    id =  db.Column(db.Integer, Identity(), primary_key = True)
    category = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return self.category
    

class Author(db.Model):
    id =  db.Column(db.Integer, Identity(),  primary_key = True)
    author_name = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return self.author_name


class Post(db.Model):
    id =  db.Column(db.Integer, Identity(start= 1, increment=1),  primary_key = True)
    post_title = db.Column(db.String(100), nullable = False)
    post_body = db.Column(db.Text)
    cover = db.Column(db.Text)
    category = db.Column(ForeignKey(Categories.id))
    author = db.Column(ForeignKey(Author.id))
    post_date = db.Column(db.DateTime, default = datetime.utcnow)
    slug = db.Column(db.String(400), nullable = False)
    status = db.Column(Boolean())
   

    def __str__(self):
        return self.post_title
    


class Comments(db.Model):
    id =  db.Column(db.Integer, Identity(), primary_key = True)
    name = db.Column(db.String(200), nullable= False)
    username = db.Column(db.String(200), nullable= False)
    email =db.Column(db.String(200))
    comment = db.Column(db.String(200), nullable= False)
    post = db.Column(ForeignKey(Post.id))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    approval_status= db.Column(Boolean())
    
    def get_queryset(self):
        queryset = super(Comments, self).get_queryset().filter(approval_status = True)
        return queryset

    def __repr__(self):
        return self.comment


class Replies(db.Model):
    id =  db.Column(db.Integer, Identity(), primary_key = True)
    name = db.Column(db.String(200), nullable= False)
    username = db.Column(db.String(200), nullable= False)
    email = db.Column(db.String(200), nullable= False)
    website = db.Column(db.String(200), nullable= False)
    reply =  db.Column(db.String(200), nullable= False)
    main_comment = db.Column(ForeignKey(Comments.id))
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "Replied to: " + str(self.main_comment)


class Contact(db.Model):
    id =  db.Column(db.Integer, Identity(), primary_key = True)
    contact_name =  db.Column(db.String(200), nullable= False)
    contact_email = db.Column(db.String(200))
    subject = db.Column(db.String(200), nullable= False)
    message = db.Column(db.String(200), nullable= False)

    def __repr__(self):
        return self.contact_name + ' :: ' + self.subject
    