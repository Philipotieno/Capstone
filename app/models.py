from app import db


class Actor(db.Model):
    """ This calss represents the actors table"""

    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def __init__(self, name, age, gender):
        """initialize with name."""
        self.name = name
        self.age = age
        self.gender = gender

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    """ This calss represents the movies table"""

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    release_date = db.Column(db.DateTime)

    def __init__(self, title, release_date):
        """initialize with name."""
        self.title = title
        self.release_date = release_date

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Movies.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Movie: {}>".format(self.title)
