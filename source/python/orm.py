#!/mnt/e/python/jumpserver/.venv/bin/python -i
import os,django

if __name__ == '__main__':
    pj_dir = ''
    pj_name = ''
    os.chdir(pj_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(pj_name))
    django.setup()
    from rest_framework.authtoken.models import Token
    from assets.models import *
    from users.models.user import User
    

