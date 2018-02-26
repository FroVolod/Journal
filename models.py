from app import db
from flask import request
from datetime import datetime
import re
from flask_security import UserMixin, RoleMixin





def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)



articles_reviews = db.Table('articles_reviews',
                            db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                            db.Column('review_id', db.Integer, db.ForeignKey('review.id'))
                            )


articles_coauthors = db.Table('articles_coauthors',
                              db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                              db.Column('coauthor_id', db.Integer, db.ForeignKey('coauthor.id'))
                              )

'''''
class Articles_authors(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    role       = db.Column(db.String(20))
    author_id  = db.Column(db.Integer, db.ForeignKey('author.id'))
'''



class Author(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    f_name  = db.Column(db.String(80))
    l_name  = db.Column(db.String(80))
    email   = db.Column(db.String(120), unique = True)
    phone   = db.Column(db.String(30))
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    organization = db.Column(db.Text)
    slug = db.Column(db.String(250), unique = True)

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.l_name:
            s = self.l_name + ' ' + self.f_name
            self.slug = slugify(s)


    def __repr__(self):
        return '{} {}, {}'.format(self.l_name, self.f_name, self.organization)


class Coauthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(80))
    l_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(30))
    organization = db.Column(db.Text)
    slug = db.Column(db.String(250), unique=True)

    def __init__(self, *args, **kwargs):
        super(Coauthor, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.l_name:
            s = self.l_name + ' ' + self.f_name
            self.slug = slugify(s)

    def __repr__(self):
        return '{} {}, {}'.format(self.l_name, self.f_name, self.organization)


class Article(db.Model):
    id           = db.Column(db.Integer, primary_key = True)
    article_name = db.Column(db.String(250))
    slug         = db.Column(db.String(250), unique = True)
    #co_author    = db.Column(db.Text)
    num_pages    = db.Column(db.Integer)
    review       = db.Column(db.Boolean())
    created      = db.Column(db.DateTime, default = datetime.now())
    file_name    = db.Column(db.Text)
    upload_date  = db.Column(db.DateTime, default = datetime.now())
    update_file  = db.Column(db.DateTime, default = datetime.now())
    annotation   = db.Column(db.Text)
    annotation_ua= db.Column(db.Text)
    key_words    = db.Column(db.String(250))
    key_words_ua = db.Column(db.String(250))
    reviews      = db.relationship('Review', secondary = articles_reviews, backref = db.backref('articles', lazy = 'dynamic'))
    journal_id   = db.Column(db.Integer, db.ForeignKey('journal.id'), nullable=False)
    author_id    = db.Column(db.Integer, db.ForeignKey('author.id'))
    topic_id     = db.Column(db.Integer, db.ForeignKey('topic.id'))
    coauthors    = db.relationship('Coauthor', secondary = articles_coauthors, backref='articles', lazy='dynamic')


    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self.generate_slug()


    def generate_slug(self):
        if self.article_name:
            self.slug = slugify(self.article_name)


    def __repr__(self):
        return '{}'.format(self.article_name)


class Topic(db.Model):
    id         = db.Column(db.Integer, primary_key = True)
    topic_name = db.Column(db.String(200))
    slug       = db.Column(db.String(200), unique = True)
    articles   = db.relationship('Article', backref = 'topic', lazy = 'dynamic')

    def __init__(self, *args, **kwargs):
        super(Topic, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.topic_name:
            self.slug = slugify(self.topic_name)

    def __repr__(self):
        return '{}'.format(self.topic_name)


class Journal(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    year    = db.Column(db.String(10))
    number  = db.Column(db.String(10))
    articles = db.relationship('Article', backref = 'journal', lazy = 'dynamic')
    slug = db.Column(db.String(200), unique=True)
    __mapper_args__ = {'order_by':slug.desc()}

    def __init__(self, *args, **kwargs):
        super(Journal, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.year:
            s = self.year + ' ' + self.number
            self.slug = slugify(s)

    def __repr__(self):
        return '{},  № {}'.format(self.year, self.number)




class Review(db.Model):
    id      = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(80))
    l_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(30))



users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default = True)

    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('users', lazy='dynamic'))




class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))