import os


class Configuration(object):
    DEBUG = os.getenv('JOURNAL_DEBUG', True)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
        user=os.getenv('JOURNAL_DB_USER', 'root'),
        password=os.getenv('JOURNAL_DB_PASSWORD', '1234'),
        host=os.getenv('JOURNAL_DB_HOST', 'localhost'),
        database=os.getenv('JOURNAL_DB_NAME', 'journal'),
    )
    SECRET_KEY = os.getenv('JOURNAL_SECRET_KEY', 'keysecret')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
