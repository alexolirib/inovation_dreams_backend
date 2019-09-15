from django.contrib.auth.models import User, Group, Permission

def create_data_default():

    try:
        User.objects.get(username='admin')
    except:
        User.objects.create_superuser(username='admin', email='ribeirolx17@gmail.com', password='admin')

    #pegar as permissoes
    permissions = Permission.objects.all()

    group_inventor = Group.objects.get_or_create(name='inventor')
    group_inventor[0].permissions.set(list(permissions))

    group_inventor = Group.objects.get_or_create(name='investidor')
    group_inventor[0].permissions.set(list(permissions))

