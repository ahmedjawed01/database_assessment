from django.db import models


class Population(models.Model):
    zip_code = models.CharField(max_length=6)
    five_mile_pop = models.CharField(max_length=255)
    recorded = models.DateField()
    org_user = models.CharField(max_length=255)
    modified_user = models.CharField(max_length=255)

    @property
    def return_recorded(self):
        return self.recorded.strftime('%m/%d/%Y')

    def __str__(self):
        return f'{self.zip_code}'

    class Meta:
        verbose_name = 'Population'
        verbose_name_plural = 'Populations'
        app_label = 'populations'
