import click
import random

from project import create_app, db
from flask.cli import with_appcontext

app = create_app('flask.cfg')


@app.cli.command('init-db')
@with_appcontext
def init_db_command():

    tags_series = 400
    graphics = 1000
    max_tags_per_graphic = 1000

    def fill_db(prod_db):
        random.seed(42)
        tag_names = ['{0}_{1}'.format(name, i)for i in range(tags_series) for name in ('tesla', 'mask', 'ev')]
        db_tags = []
        for element in tag_names:
            tag = Tag(element)
            db_tags.append(tag)
            prod_db.session.add(tag)
        for i in range(graphics):
            graph = Graph('G1{:05d}'.format(i))
            graph.tags.extend(random.sample(db_tags, random.randint(1, max_tags_per_graphic)))
            prod_db.session.add(graph)

    from project.models import Tag, Graph, tags
    db.create_all()
    fill_db(db)
    db.session.commit()
    click.echo('Initialized the database.')
