from app import app, db
from app.models import User, Tag

with app.app_context():
    user = User(username='testuser', email='test@example.com')
    tag = Tag(name='testtag')
    print('kghskjfhsfjsfs')