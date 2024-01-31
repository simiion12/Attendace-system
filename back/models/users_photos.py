from mongoengine import Document, StringField, ImageField


class UsersPhoto(Document):
    meta = {'collection': 'users_photos'}
    user_id = StringField(required=True, unique=True)
    user_photo = ImageField(required=True)


# inserting a new user photo
def insert_user_photo(user_id, user_photo):
    new_user_photo = UsersPhoto(user_id=user_id, user_photo=user_photo)
    new_user_photo.save()



