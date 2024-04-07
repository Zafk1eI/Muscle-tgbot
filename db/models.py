from tortoise import fields
from tortoise.models import Model


class Muscle(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=45)
    image_path = fields.CharField(max_length=75)


class User(Model):
    user_id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    answer_count = fields.IntField()


class UsersMuscles(Model):
    record_id = fields.IntField(pk=True)
    muscle_id = fields.ForeignKeyField("models.Muscle", related_name="muscle_id")
    user = fields.ForeignKeyField("models.User", related_name="muscles_user")
