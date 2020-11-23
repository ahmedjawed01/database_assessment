import csv
from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from database_assessment.utils import get_reader, write_a_csv_file_response
from populations.models import Population


class UploadAndDownloadPopulationsCSV(TemplateView):
    template_name = 'populations/pop_radius.html'
    validator = ['N/A', '', None]

    def check_file_format(self, file_name):
        if not file_name.name.endswith('.csv'):
            return self.return_message(request=self.request, msg='Not a CSV file', error=True)

    def return_message(self, request, msg, error=False):
        messages.error(request, msg) if error else messages.success(request, msg)
        return render(self.request, self.template_name)

    @transaction.atomic()
    def post(self, request):
        csv_file_download = request.FILES.get('csv_file_download', None)
        csv_file_upload = request.FILES.get('csv_file_upload', None)
        if csv_file_download:
            self.check_file_format(csv_file_download)  # Check CSV or Not
            list_data = get_reader(csv_file_download)
            zip_codes = [str(d['Zip']) for d in list_data if 'Zip' in d]
            populations = Population.objects.filter(zip_code__in=zip_codes)
            return write_a_csv_file_response(zip_codes=zip_codes, queryset=populations, diff_key='five_mile_pop',
                                             diff_key_header='5 Mile Population')
        if csv_file_upload:
            create_record_list = []
            self.check_file_format(csv_file_upload)  # Check CSV or Not
            list_data = get_reader(csv_file_upload)

            validations = []
            [validations.append(False) if
             (d.get("Zip") in self.validator or d.get("5 Mile Population") in self.validator or d.get("Recorded")
              in self.validator or d.get("ORG User") in self.validator or d.get("Modified User") in self.validator)
             else validations.append(True) for d in list_data]

            if not all(validations):
                return self.return_message(request=request, msg='Please Provide valid data. '
                                                                '\n Note: Data must not have N/A and null', error=True)
            zip_codes = [d['Zip'] for d in list_data if 'Zip' in d]
            pre_save_population = Population.objects.filter(zip_code__in=zip_codes).values_list('zip_code', flat=True)
            create_new_objects = set(zip_codes) - set(pre_save_population)

            for sub in list_data:
                if sub.get('Zip') in create_new_objects:
                    recorde = sub.pop('Recorded')
                    try:
                        date_dt2 = datetime.strptime(recorde, '%m/%d/%Y')
                    except:
                        return self.return_message(request=request, msg='Please Provide valid date eg: 1/22/2020.',
                                                   error=True)
                    create_record_list.append(Population(
                        five_mile_pop=sub.get('5 Mile Population'), recorded=date_dt2.date(), zip_code=sub.get('Zip'),
                        org_user=sub.get('ORG User'), modified_user=request.user.username
                    ))
            if create_record_list:
                Population.objects.bulk_create(create_record_list)
                return self.return_message(request=request, msg='Data Updated Successfully.')
            return self.return_message(request=request, msg='Already Up-to-date on the basis of Zip.')
        return self.return_message(request=request, msg='No file selected.', error=True)
