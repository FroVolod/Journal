from app import app
import view
from articles.blueprint import articles

app.register_blueprint(articles, url_prefix = '/journals')

if __name__ == '__main__':
    app.run()