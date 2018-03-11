import os

from app import *
from flask import render_template, request, redirect, url_for
from models import *
from wtforms.fields import FileField, SubmitField, FormField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import current_user
from articles.forms import New_Author


def co_author(author):
    print('Проверка входа в def co_author')
    if request.method == 'POST' and request.form['f_name']:
        print('Проверка reques.method:', request.method)
        author = request.form
        print(author['org'])
        coauthor = Coauthor.query.filter(Coauthor.f_name == author['f_name']).first()
        if coauthor:
            coauthor.f_name = author['f_name']
            coauthor.l_name = author['l_name']
            coauthor.organization = author['org']
            coauthor.stepen = author['stepen']
            coauthor.zvanie = author['zvanie']
            coauthor.dolzh = author['dolzh']
            #coauthor.organization = Organization.query.filter(Organization.id == author['organization']).first().name
            coauthor.email = author['email']
            coauthor.phone = author['phone']
            #coauthor.slug = author.slug
            db.session.merge(coauthor)
        else:
            coauthor = Coauthor(f_name=author['f_name'], l_name=author['l_name'], organization=author['org'],
                                email=author['email'], phone=author['phone'], stepen = author['stepen'],
                                zvanie = author['zvanie'], dolzh = author['dolzh'])
            db.session.add(coauthor)
        db.session.commit()



@app.route('/')
def index():
    name = 'Volodymyr'

    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        articles = Article.query.filter(Article.article_name.contains(q) | Article.annotation.contains(q) | Article.key_words.contains(q))
    else:
        return render_template('index.html', n=name)

    pages = articles.paginate(page=page, per_page=5)

    return render_template('articles/articles.html', articles=articles, pages=pages)







class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next = request.url))

class BaseModelView(ModelView):
    page_size = 14
    column_exclude_list = ('slug')
    create_modal = True
    edit_modal = True
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class ArticleAdminView(AdminMixin, BaseModelView):
    column_searchable_list = ('authors', 'article_name', 'org', 'file_name')
    column_labels = dict(org='Організація', authors = 'Автор', article_name = 'Назва статті', topic = 'Розділ',
                         created = 'Подано', file_name = 'Назва файлу', update_file = 'Зміна файлу', review = 'До друку',
                         journal = 'Номер журналу', author = 'Автор', coauthors = 'Співавтори', num_pages = 'Сторінки',
                         annotation_ua = 'Анотація', annotation = 'Annotation', key_words_ua = 'Ключові слова',
                         key_words = 'Keywords')
    column_list = ('authors', 'org', 'article_name', 'topic', 'created', 'file_name', 'update_file', 'review')
    #column_sortable_list = ('file_name')
    #column_default_sort = 'author'
    can_view_details = True
    column_default_sort =('created', True)
    form_columns = ['journal', 'author', 'coauthors', 'topic', 'article_name', 'num_pages', 'annotation_ua',
                    'annotation', 'key_words_ua', 'key_words', 'file']
    #form_args = dict(journal=dict(default=(Journal.query.order_by(Journal.id.desc()).first().id)))
    form_extra_fields = {'file': FileField('File (.doc, .docx, .pdf)')}
    new_author = FormField(New_Author)



    def on_model_change(self, form, model, is_created):
        try:
            if request.method == 'POST':
                file = request.files['file']
                if os.path.splitext(file.filename)[1] not in ('.pdf', '.docx', '.doc'):
                    print("Incorrect filename: '%s'" % file.filename)
                    print(os.path.splitext(file.filename)[1])
                    return redirect('/')

                jour = request.form['journal']
                journal = Journal.query.filter(Journal.id == jour).first()
                author = Author.query.filter(Author.id == request.form['author']).first()
                model.org = author.org
                model.authors = author.l_name + ' ' + author.f_name
                print(file.filename.rsplit('.', 1)[1])
                print(author.org)
                print(author.f_name)
                print(author.l_name)
                print(journal.slug)
                file_name =re.sub(r'[^\w+]', '_', journal.slug + '_' + author.l_name + '_' + author.f_name + '_' + author.org)\
                                    + str(os.path.splitext(file.filename)[1])
                print(author.org)
                print(file_name)
                try:
                    print('journal  ', journal)
                    model.file_name = file_name
                    model.update_file = datetime.now()
                    file.save('pdf_files/' + file_name)
                except:
                    print('Внимание! Ошибка')
        except Exception as e:
            print(e)
            raise

        return super(ArticleAdminView, self).on_model_change(form, model, is_created)

class TopicAdminView(AdminMixin, BaseModelView):
    column_default_sort = 'topic_name'
    form_columns = ['topic_name']


class AuthorAdminView(AdminMixin, BaseModelView):
    column_searchable_list = ('l_name', 'f_name', 'org', 'email', 'phone')
    column_default_sort = 'l_name'
    column_labels = dict(org = 'Організація', l_name = 'Призвище', f_name = "Ім'я", stepen = 'Науковий ступінь',
                         zvanie = 'Наукове звання', dolzh = 'Посада', phone = 'Телефон')
    column_list = ('f_name', 'l_name', 'stepen', 'zvanie', 'dolzh', 'org', 'email', 'phone')
    form_columns = ['f_name', 'l_name', 'stepen', 'zvanie', 'dolzh', 'org', 'email', 'phone']

    #inline_models = [(Article, dict(form_columns = ['id', 'journal', 'article_name', 'annotation_ua', 'annotation_ua', 'key_words_ua', 'key_words', 'topic']))]


    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        co_author(self)
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class JournalAdminView(AdminMixin, BaseModelView):
    form_columns = ['year', 'number']





class AdminView(AdminMixin, ModelView):
    pass

class AdminHomeView(AdminMixin, AdminIndexView):
    pass


admin.add_view(AuthorAdminView(Author, db.session))
admin.add_view(ArticleAdminView(Article, db.session))
admin.add_view(TopicAdminView(Topic, db.session))
admin.add_view(JournalAdminView(Journal, db.session))