from flask import Blueprint, request
from app.models import Category, Question, Word

bp = Blueprint('api', __name__, url_prefix="/api")


@bp.get('/')
def index():
    return {'everything': 'ok'}


@bp.get('/categories/')
def categories():
    category = Category()

    res = category.get_all()

    return {'result': [item.__json__() for item in res]}


@bp.get('/category/<category_id>/question/')
def question(category_id):
    question_model = Question()
    limit = request.args.get('limit', '1')
    limit = int(limit) if limit.isnumeric() else 1

    questions = question_model.where('category_id',
                                    category_id).order_by('RANDOM()').limit(limit).get_all()

    return {
        'result': [question.__json__() for question in questions],
        'limit': limit
    }

@bp.get('/category/<category_id>/word/')
def word(category_id):
    word_model = Word()

    word = word_model.where('category_id',
                                    category_id).order_by('RANDOM()').first()
    if word is None:
        return {'error': f'No word founded for category "{category_id}".'}

    return {
        'result': word.__json__(),
    }
