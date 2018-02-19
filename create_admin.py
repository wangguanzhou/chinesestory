# python manage.py shell

from django.contrib.auth.models import User

user = User.object.create_user('bsdadmin', 'bsdadmin@6677ba.ca', 'chinese123')
user.save()

user = User.object.create_user('logadmin', 'logadmin@6677ba.ca', 'chinese456')
user.save()

user = User.object.create_user('mtladmin', 'mtladmin@6677ba.ca', 'chinese789')
user.save()

user = User.object.create_user('cdnadmin', 'cdnadmin@6677ba.ca', 'chinese777')
user.save()
