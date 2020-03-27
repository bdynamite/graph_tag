import pytest
from project import create_app, db
from project.models import Tag, Graph


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    def fill_test_db(test_db):
        tag_names = [
            'one',
            'two',
            'three',
        ]
        db_tags = []
        for element in tag_names:
            tag = Tag(element)
            db_tags.append(tag)
            test_db.session.add(tag)
        for i in range(3):
            graph = Graph('G1{:05d}'.format(i))
            graph.tags.extend(db_tags[:i + 1])
            test_db.session.add(graph)

    fill_test_db(db)
    db.session.commit()

    yield db

    db.drop_all()
