from django.contrib import admin
from django import forms
from bb_products.models import BBProduct


class BBProductAdminForm(forms.ModelForm):
    class Meta:
        model = BBProduct
        fields = '__all__'


class BBProductAdmin(admin.ModelAdmin):
    form = BBProductAdminForm
    list_display = ['zip_code', 'product', 'recorded', 'org_user', 'modified_user']


admin.site.register(BBProduct, BBProductAdmin)
