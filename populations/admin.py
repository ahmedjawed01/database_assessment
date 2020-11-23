from django.contrib import admin

from populations.models import Population
from django import forms


class PopulationAdminForm(forms.ModelForm):
    class Meta:
        model = Population
        fields = '__all__'


class PopulationAdmin(admin.ModelAdmin):
    form = PopulationAdminForm
    list_display = ['zip_code', 'five_mile_pop', 'recorded', 'org_user', 'modified_user']


admin.site.register(Population, PopulationAdmin)
