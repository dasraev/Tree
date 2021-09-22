import json
import os
from django.core.management import BaseCommand
from django.db import transaction
from django.conf import settings
from django.db import IntegrityError
BASE_DIR = settings.BASE_DIR
from dreeapp import models





def load_regions():
    with open(os.path.join(BASE_DIR, 'common_region.json'), encoding="utf8",
              errors='ignore') as json_file:
        data = json.load(json_file)
        for region_data in data:
            try:
                models.Region.objects.create(id=region_data['id'], title=region_data['name'],)
            except IntegrityError:
                region = models.Region.objects.get(id=region_data['id'])
                region.title = region_data['name']
                region.save()
    return models.Region.objects.all()


def load_districts():
    with open(os.path.join(BASE_DIR, 'common_district.json'), encoding="utf8",
              errors='ignore') as json_file:
        data = json.load(json_file)
        for district in data:
            try:
                models.District.objects.create(id=district['id'], title=district['name'],
                                               region_id=district['region_id'])
            except IntegrityError:
                district = models.Region.objects.get(id=district['id'])
                district.title = district['name']
                district.region_id = district['region_id']
                district.save()
    return models.District.objects.all()



def load_mahalla():
    with open(os.path.join(BASE_DIR, 'gatherings.json'), encoding="utf8",
              errors='ignore') as json_file:
        data = json.load(json_file)
        for mahalla_data in data:
            try:
                models.Mahalla.objects.create(id=mahalla_data['id'], title=mahalla_data['name'],
                                               district_id=mahalla_data['district_id'])
            except IntegrityError:
                mahalla = models.Mahalla.objects.get(id=mahalla_data['id'])
                mahalla.title = mahalla_data['name']
                mahalla.district_id = mahalla_data['district_id']
                mahalla.save()

    return models.District.objects.all()


from django.utils import timezone

class Command(BaseCommand):
    help = 'Cron testing'

    def handle(self, *args, **options):
        with transaction.atomic():
            regions = load_regions()
            districts = load_districts()
            mahalla = load_mahalla()
        self.stdout.write(self.style.SUCCESS("Successfully imported regions and districts"))
