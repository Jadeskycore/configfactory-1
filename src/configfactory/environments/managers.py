from django.db import models


class EnvironmentQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)


class EnvironmentManager(models.Manager):

    def get_queryset(self):
        return EnvironmentQuerySet(
            model=self.model,
            using=self.db
        )

    def active(self):
        return self.get_queryset().active()
