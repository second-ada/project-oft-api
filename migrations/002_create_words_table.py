from app.database import db


class Migration_CreateWordsTable(db.Migration):

    def up(self):
        db.create_table(
            'words', [
                db.Column(
                    'id', db.INTEGER, primary_key=True, autoincrement=True
                ),
                db.Column('word', db.TEXT, unique=True, nullable=False),
                db.Column('category_id', db.INTEGER, nullable=False),
                db.Column('created_at', db.TEXT, default="CURRENT_TIMESTAMP"),
            ]
        )
        super().up()

    def down(self):
        db.drop_table('words')
        super().down()


"""
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE,
    color TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    category_id INTEGER,
    created_at TIMESTAMP
);
"""
