from peewee import *


db = SqliteDatabase('requests.db')


class Request(Model):
    """
    Класс базы данных запросов пользователей.
    """
    id = PrimaryKeyField()
    user_name = CharField(null=True)
    command = CharField()
    location = CharField()
    from_price = IntegerField(null=True)
    to_price = IntegerField(null=True)
    from_distance = FloatField(null=True)
    to_distance = FloatField(null=True)
    result_range = IntegerField()
    photos = BooleanField()
    photos_amount = IntegerField(null=True)
    from_date = DateField()
    to_date = DateField()
    date_of_request = DateTimeField()
    hotels_found = CharField(null=True)

    class Meta:
        database = db
