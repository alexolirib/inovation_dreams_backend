from django.db import models


class UserContactManage(models.Manager):

    def bulk_create_or_update(self, list_user_contact):
        for user_contact in list_user_contact:
            if user_contact.contact.id is None:
                user_contact.contact.save()
                user_contact.contact_id = user_contact.contact.id
            else:
                user_contact.contact.save()

            user_contact.save()
