from django.conf import settings
from django.db import models


class EnvironmentQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    def base(self):
        return self.filter(alias=settings.BASE_ENVIRONMENT)


class EnvironmentManager(models.Manager):

    def get_queryset(self):
        return EnvironmentQuerySet(
            model=self.model,
            using=self.db
        )

    def active(self):
        return self.get_queryset().active()

    def base(self):
        return self.get_queryset().base()
