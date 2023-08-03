import peewee

db = peewee.PostgresqlDatabase(
    "postgres",
    user="postgres",
    password="postgrespw",
    host="localhost",
    port="55006",
)


class Message(peewee.Model):
    message = peewee.TextField()

    class Meta:
        database = db


class Feedback(peewee.Model):
    firstname = peewee.TextField()
    lastname = peewee.TextField()
    phone = peewee.TextField()
    email = peewee.TextField()
    description = peewee.TextField()
    rating = peewee.TextField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Message, Feedback])


def insert_feedback(firstname, lastname, phone, email, description, rating):
    feedback = Feedback(
        firstname=firstname,
        lastname=lastname,
        phone=phone,
        email=email,
        description=description,
        rating=rating,
    )
    feedback.save()


def main():
    create_tables()


if __name__ == "__main__":
    main()
