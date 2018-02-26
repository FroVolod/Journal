import os

from app import *
from flask import render_template, request, redirect, url_for
from models import *
from wtforms.fields import FileField, SubmitField, FormField
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_security import current_user
from articles.forms import New_Author


def co_author(self):
    print('Проверка входа в def co_author')
    if request.method == 'POST' and request.form['f_name']:
        print('Проверка reques.method:', request.method)
        coauthor = Coauthor.query.filter(Coauthor.slug == self.slug).first()
        if coauthor:
            coauthor.f_name = self.f_name
            coauthor.l_name = self.l_name
            coauthor.organization = self.organization
            coauthor.email = self.email
            coauthor.phone = self.phone
            db.session.merge(coauthor)
        else:
            coauthor = Coauthor(f_name=self.f_name, l_name=self.l_name, organization=self.organization,
                                email=self.email, phone=self.phone)
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
    #create_modal = True
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class ArticleAdminView(AdminMixin, BaseModelView):
    column_list = ('author', 'article_name', 'topic', 'file_name', 'created')
    #column_sortable_list = ('file_name')
    #column_default_sort = 'author'
    can_view_details = True
    column_default_sort =('created', True)
    form_columns = ['journal', 'author', 'coauthors', 'article_name', 'annotation_ua', 'annotation_ua', 'key_words_ua', 'key_words', 'topic', 'file']
    #form_args = dict(journal=dict(default=(Journal.query.order_by(Journal.id.desc()).first().id)))
    form_extra_fields = {'file': FileField('File (.pdf)')}
    new_author = FormField(New_Author)



    def on_model_change(self, form, model, is_created):
        if request.method == 'POST':
            file = request.files['file']
            if os.path.splitext(file.filename)[1] != '.pdf':
                print("Incorrect filename: '%s'" % file.filename)
                return redirect('/')

            jour = request.form['journal']
            journal = Journal.query.filter(Journal.id == jour).first()
            author = Author.query.filter(Author.id == request.form['author']).first()
            print(file.filename.rsplit('.', 1)[1])
            file_name = re.sub(r'[^\w+]', '_', journal.slug + '_' + author.l_name + '_' + author.f_name + '_' + author.organization) + '.pdf'
            try:
                print('journal  ', journal)
                model.file_name = file_name
                file.save('pdf_files/' + file_name)
            except:
                print('Внимание! Ошибка')

        return super(ArticleAdminView, self).on_model_change(form, model, is_created)

class TopicAdminView(AdminMixin, BaseModelView):
    column_default_sort = 'topic_name'
    form_columns = ['topic_name']

class AuthorAdminView(AdminMixin, BaseModelView):
    column_default_sort = 'l_name'
    column_list = ('l_name', 'f_name', 'organization', 'email', 'phone')
    form_columns = ['l_name', 'f_name', 'organization', 'email', 'phone']

    inline_models = [(Article, dict(form_columns = ['id', 'journal', 'article_name', 'annotation_ua', 'annotation_ua', 'key_words_ua', 'key_words', 'topic']))]


    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        model.co_author()
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