from project import db


tags = db.Table(
    'graph_tags',
    db.Column('graph_id', db.String(7), db.ForeignKey('graph.id')),
    db.Column('tag_id', db.String(20), db.ForeignKey('tag.id')),
)


class Graph(db.Model):
    id = db.Column(db.String(7), primary_key=True, unique=True)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('graphs', lazy='dynamic'))

    def __init__(self, idx):
        self.id = idx

    def __repr__(self):
        return '<Graph {}>'.format(self.id)


class Tag(db.Model):
    id = db.Column(db.String(20), primary_key=True, unique=True)

    def __init__(self, idx):
        self.id = idx

    def __repr__(self):
        return '<Tag {}>'.format(self.id)
