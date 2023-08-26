from faker import Faker
from app.database import db
from app.models import Category, Word, Question

faker = Faker('pt_BR')

random_colors = [
    "#E57373", "#81C784", "#64B5F6", "#FFD54F", "#9575CD", "#4DB6AC",
    "#FF8A65", "#7986CB", "#A1887F", "#4DD0E1"
]

for i in range(10):
    word = faker.unique.word()

    category = Category(
        title=word,
        slug=word.lower().replace(' ', '_'),
        color=random_colors.pop()
    )
    category.save()

for category_id in range(1, 11):
    for j in range(10):
        word = Word(word=faker.unique.word(), category_id=category_id)
        word.save()

for category_id in range(1, 11):
    for j in range(10):
        question = Question(
            question=faker.text(max_nb_chars=80)[:-1] + '?',
            category_id=category_id
        )
        question.save()

db.conn.commit()
