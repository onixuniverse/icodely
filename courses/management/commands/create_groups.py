import logging

from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


GROUPS = ["teacher"]
MODELS_CODENAME = ["course", "lesson", "inviteurl"]
PERMISSIONS = ["add", "change", "delete", "view"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model_codename in MODELS_CODENAME:
                for permission in PERMISSIONS:
                    codename = "{}_{}".format(permission, model_codename)
                    print("Creating {}".format(model_codename))

                    try:
                        model_add_perm = Permission.objects.get(codename=codename)
                    except:
                        logging.warning("Permission not found with name {}.".format(codename))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")
