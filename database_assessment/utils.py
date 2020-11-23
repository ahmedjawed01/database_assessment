import csv

from django.http import HttpResponse


def get_reader(file):
    return list(csv.DictReader(file.read().decode('utf-8').splitlines()))


def write_a_csv_file_response(zip_codes, queryset, diff_key, diff_key_header):
    DIFF_KEY = diff_key
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'
    writer = csv.writer(response)
    writer.writerow(['Zip', diff_key_header, 'Recorded', 'ORG User', 'Modified User'])
    for zip in zip_codes:
        query_obj = queryset.filter(zip_code__exact=zip).first()
        writer.writerow(
            [f'="{query_obj.zip_code}"', getattr(query_obj, DIFF_KEY), query_obj.return_recorded,
             query_obj.org_user, query_obj.modified_user]) \
            if query_obj else writer.writerow([f'="{zip}"', 'N/A', 'N/A', 'N/A', 'N/A'])
    return response
