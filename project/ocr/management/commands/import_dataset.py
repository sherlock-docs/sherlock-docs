import os

from django.core.management import BaseCommand
from django.core.files import File

from ocr.models import Document, PageDocument


class Command(BaseCommand):
    def handle(self, *args, **options):
        Document.objects.all().delete()
        PageDocument.objects.all().delete()
        dataset_path = os.path.join("/user", "src", "app", "Dataset")
        for file_type in os.listdir(dataset_path):
            path_to_file = os.path.join(dataset_path, file_type)
            for file in os.listdir(path_to_file):
                filepath = os.path.join(path_to_file, file)
                page, created = Document.objects.get_or_create(file=filepath)
                # Прикладываем файл.
                with open(filepath, 'rb') as f:
                    page.file.save(file, File(f), save=True)