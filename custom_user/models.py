from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    DEFAULT = 0
    BB_PRODUCT = 1
    POPULATION = 2

    USER_CHECK = (
        (DEFAULT, 'Default'),
        (BB_PRODUCT, 'BB Product'),
        (POPULATION, 'Population')
    )
    db_role = models.PositiveIntegerField(
        choices=USER_CHECK, default=DEFAULT, verbose_name="\nFor which database you want to create this user.\nUse any one role:\n\n0 for Super Admin User.\n1 for BB Product User.\n2 for Population User.\nEnter your selection"
    )

    REQUIRED_FIELDS = ['db_role']
