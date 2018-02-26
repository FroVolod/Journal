from flask import Blueprint, render_template, request, redirect, url_for
from models import *
from articles.forms import New_Article


articles = Blueprint('articles', __name__, template_folder = 'templates')


@articles.route('/')
def index():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    journals = Journal.query.order_by(Journal.slug.desc())

    pages = journals.paginate(page=page, per_page=10)

    return render_template('articles/index.html', journals=journals, pages=pages)


@articles.route('/<slug>')
def journal_detail(slug):
    journal = Journal.query.filter(Journal.slug == slug).first()
    articles = journal.articles.all()[::-1]

    return render_template('articles/journal_detail.html', number = journal.number, year = journal.year, articles = articles)


@articles.route('/article/<slug>')
def article_detail(slug):
    article = Article.query.filter(Article.slug == slug).first()
    return render_template('articles/article_detail.html', article = article)


@articles.route('/articles')
def art():
    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        articles = Article.query.filter(Article.article_name.contains(q) | Article.annotation.contains(q) | Article.key_words.contains(q))
    else:
        articles = Article.query.order_by(Article.created.desc())

    pages = articles.paginate(page=page, per_page=5)

    return render_template('articles/articles.html', articles=articles, pages=pages)


@articles.route('/create', methods = ['GET', 'POST'])
def create_article():
    print('проверка')
    form = New_Article()
    print('проверка 1')
    if form.validate_on_submit():
        print('проверка 2')
        return redirect(url_for('index.html'))
    return render_template('articles/create_article.html', form = form)