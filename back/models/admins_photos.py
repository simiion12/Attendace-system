#from back.models import mongo
from mongoengine import Document, StringField, FileField


class AdminsPhoto(Document):
    filename = StringField(required=True, unique=True)
    admin_id = StringField(required=True, unique=True)
    admin_photo = FileField(required=True)
