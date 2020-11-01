import re
import time
import hashlib
from django.db import connections
from django.core.cache import cache
from collections import OrderedDict
from django.core.management import BaseCommand
from django.db import connections
from django.conf import settings
import os
import glob
import pathlib
from .models import Document, PageDocument

class Command(BaseCommand):
    def handle(self, *args, **options):
        Document.objects.all().delete()
        PageDocument.objects.all().delete()
        dataset_files = os.path.join(settings.BASE_DIR, "media", "Dataset")
        for file_type in os.listdir(dataset_files):
            path_to_file = os.path.join(dataset_files, file_type)
            for file in os.listdir(path_to_file):
                filepath = os.path.join(path_to_file, file)
                Document.objects.get_or_create(file_type=file_type, file=filepath)