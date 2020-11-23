import csv
from datetime import datetime

from django.core.management import call_command
from django.core.management.commands.migrate import Command as CoreMigrateCommand
from bb_products import models
from populations.models import Population


def create_bb_products_constraints():
    from django.conf import settings
    print("Executing BB Product migrate Command.")

    fixture_path = settings.BASE_DIR / 'bb_products/fixtures/BB_product_master.csv'
    with open(fixture_path, mode='r') as csv_file:
        list_data =list(csv.DictReader(csv_file))
        zip_codes = [str(d['Zip']) for d in list_data if 'Zip' in d]
        bb_products = models.BBProduct.objects.filter(zip_code__in=zip_codes).values_list('zip_code', flat=True)
        remain = set(zip_codes) - set(bb_products)
        create_record_list = []
        for sub in list_data:
            if sub.get('Zip') in remain:
                date = datetime.strptime(sub.pop('Recorded'), '%m/%d/%Y')
                create_record_list.append(models.BBProduct(
                    product=sub.get('Product'), recorded=date, zip_code=sub.get('Zip'),
                    org_user=sub.get('ORG User'), modified_user=sub.get('Modified User')
                ))
        if create_record_list:
            models.BBProduct.objects.bulk_create(create_record_list)
            print(f"Created {len(create_record_list)} objects.")


def create_population_constraints():
    from django.conf import settings
    print("Executing POP migrate Command.")
    fixture_path = settings.BASE_DIR / 'populations/fixtures/Zip_POP_master.csv'
    with open(fixture_path, mode='r') as csv_file:
        list_data =list(csv.DictReader(csv_file))
        zip_codes = [str(d['Zip']) for d in list_data if 'Zip' in d]
        populations = Population.objects.filter(zip_code__in=zip_codes).values_list('zip_code', flat=True)
        remain = set(zip_codes) - set(populations)
        create_record_list = []
        for sub in list_data:
            if sub.get('Zip') in remain:
                date = datetime.strptime(sub.pop('Recorded'), '%m/%d/%Y')
                create_record_list.append(Population(
                    five_mile_pop=sub.get('5 Mile Population'), recorded=date.date(), zip_code=sub.get('Zip'),
                    org_user=sub.get('ORG User'), modified_user=sub.get('Modified User')
                ))
        if create_record_list:
            Population.objects.bulk_create(create_record_list)
            print(f"Created {len(create_record_list)} objects.")


class Command(CoreMigrateCommand):
    def handle(self, *args, **options):
        # Do normal migrate
        super().handle(*args, **options)
        database = options['database']
        if database == 'bb_product':
            # Then our custom extras
            create_bb_products_constraints()

        elif database == 'population':
            # Then our custom extras
            create_population_constraints()
        else:
            call_command('migrate', '--database=population')
            call_command('migrate', '--database=bb_product')

