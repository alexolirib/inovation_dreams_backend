from django.db import models


class UsuarioManager(models.Manager):
    def get_user_fom_user_auth_json(self, user_auth):

        user = self.get(auth_user=user_auth)
        from usuario.models import UserContact
        users_contacts = UserContact.objects.filter(usuario=user)
        address_json = user.address.__dict__
        address_json.pop('_state')
        address_json.pop('id')

        usuario_contact_json = []
        if len(users_contacts) > 0:
            for user_contact in users_contacts:
                usuario_contact_json.append({
                    "type": user_contact.contato.type,
                    "value": user_contact.contato.value
                })
        user_json = user.__dict__

        user_json.pop('_state')
        user_json.pop('auth_user_id')
        user_json.pop('address_id')

        json = {
            "email": user_auth.email,
            **user_json,
            "contacts": usuario_contact_json,
            "address": {**address_json}
        }
        return json
