from django.db import models


class BBProduct(models.Model):
    zip_code = models.CharField(max_length=6)
    product = models.CharField(max_length=255)
    recorded = models.DateField()
    org_user = models.CharField(max_length=255)
    modified_user = models.CharField(max_length=255)

    @property
    def return_recorded(self):
        return self.recorded.strftime('%m/%d/%Y')

    def __str__(self):
        return f'{self.zip_code}'

    class Meta:
        verbose_name = 'BB-Product'
        verbose_name_plural = 'BB-Products'
        app_label = 'bb_products'
