import csv
from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from bb_products.models import BBProduct
from database_assessment.utils import get_reader, write_a_csv_file_response


class UploadAndDownloadBBProductCSV(TemplateView):
    template_name = 'bb_products/products.html'
    validator = ['N/A', '', None]

    def check_file_format(self, file_name):
        if not file_name.name.endswith('.csv'):
            messages.error(self.request, 'Not a CSV file.')
            return render(self.request, self.template_name)

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
            bb_products = BBProduct.objects.filter(zip_code__in=zip_codes)

            # Create the HttpResponse object with the appropriate CSV header.
            return write_a_csv_file_response(
                zip_codes=zip_codes, queryset=bb_products, diff_key='product', diff_key_header='Product')

        if csv_file_upload:
            create_record_list = []
            self.check_file_format(csv_file_upload)  # Check CSV or Not
            list_data = get_reader(csv_file_upload)

            validations = []
            [validations.append(False) if (
                    d.get("Zip") in self.validator or d.get("Product") in self.validator or d.get("Recorded")
                    in self.validator or d.get("ORG User") in self.validator or d.get("Modified User") in
                    self.validator) else validations.append(True) for d in list_data]

            if not all(validations):
                return self.return_message(request=request, msg='Please Provide valid data. \n '
                                                                'Note: Data must not have N/A and null', error=True)

            zip_codes = [d['Zip'] for d in list_data if 'Zip' in d]
            pre_save_bb_product = BBProduct.objects.filter(zip_code__in=zip_codes).values_list('zip_code', flat=True)
            new_objects = set(zip_codes) - set(pre_save_bb_product)

            for sub in list_data:
                if sub.get('Zip') in new_objects:
                    recorde = sub.pop('Recorded')
                    try:
                        date_dt2 = datetime.strptime(recorde, '%m/%d/%Y')
                    except:
                        return self.return_message(request=request, msg='Please Provide valid date eg: 1/22/2020.',
                                                   error=True)
                    create_record_list.append(BBProduct(
                        product=sub.get('Product'), recorded=date_dt2.date(), zip_code=sub.get('Zip'),
                        org_user=sub.get('ORG User'), modified_user=request.user.username
                    ))
            if create_record_list:
                BBProduct.objects.bulk_create(create_record_list)
                return self.return_message(request=request, msg='Data Updated Successfully.')
            return self.return_message(request=request, msg='Already Up-to-date on the basis of Zip.')
        return self.return_message(request=request, msg='No file selected.', error=True)
