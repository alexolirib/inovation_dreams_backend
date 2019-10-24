from django.db import models


class UserContactManage(models.Manager):

    def bulk_create_or_update(self, list_user_contact):
        for user_contact in list_user_contact:
            user_contact.contact.save()
            user_contact.save()
