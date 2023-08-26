from app.database import db


class Category(db.Model):
    __table__ = 'categories'
    primary_key = 'id'
    fields = ['id', 'title', 'slug', 'color']

    def __repr__(self):
        return f'<Category id="{self.id}" title="{self.title}">'


class Word(db.Model):
    __table__ = 'words'
    primary_key = 'id'
    fields = ['id', 'word', 'category_id']


class Question(db.Model):
    __table__ = 'questions'
    primary_key = 'id'
    fields = ['id', 'question', 'category_id']
