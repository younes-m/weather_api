from api import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
        self.temp_k = None

    def __repr__(self):
        return '<Name %r>' % self.name

    @property
    def temp_c(self):
        if not self.temp_k:
            return None

        return self.temp_k - 273.15

    @property
    def temp_f(self):
        if not self.temp_k:
            return None

        return 1.8*(self.temp_k - 273) + 32

    def serialize(self):
        return {"id": self.id, "name": self.name, "temp_k": self.temp_k, "temp_f": self.temp_f, "temp_c": self.temp_c}


def init_db():
    db.create_all()
    for name in ["rennes", "leipzig", "vienna", "prague", "paris", "madrid", "london", "new york", "roma", "sydney"]:
        city = City(name)
        db.session.add(city)
    db.session.commit()


if __name__ == '__main__':
    init_db()
