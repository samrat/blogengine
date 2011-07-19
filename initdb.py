from flaskext.sqlalchemy import SQLAlchemy
from blogengine import create_app

app = create_app()
db = SQLAlchemy()

__all__ = ['db']

with app.test_request_context():
    db.create_all()
