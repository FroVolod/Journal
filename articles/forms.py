from flask_wtf import FlaskForm
from wtforms import StringField, validators
from models import Author



class New_Author(FlaskForm):
    name    = StringField('Name')
    organization = StringField('Organization')


class New_Article(FlaskForm):
    l_name = StringField('Фамилия')
    f_name = StringField('Имя')
    f2_name = StringField('Отчество')
    organization = StringField('Организация')
    email = StringField('e-mail', [validators.Email("Необходимо ввести корректный E-mail")])
    journal = StringField('Номер журнала')
