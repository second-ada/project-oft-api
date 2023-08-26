from app.database import db


class Migration_CreateQuestionsTable(db.Migration):

    def up(self):
        db.create_table(
            'questions', [
                db.Column(
                    'id', db.INTEGER, primary_key=True, autoincrement=True
                ),
                db.Column('question', db.TEXT, unique=True, nullable=False),
                db.Column('category_id', db.INTEGER, nullable=False),
                db.Column('created_at', db.TEXT, default="CURRENT_TIMESTAMP"),
            ]
        )
        super().up()

    def down(self):
        db.drop_table('questions')
        super().down()
