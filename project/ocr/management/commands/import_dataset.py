import os
from django.core.management import BaseCommand
from ocr.models import Document, PageDocument
from django.core.files import File

class Command(BaseCommand):
    def handle(self, *args, **options):
        Document.objects.all().delete()
        PageDocument.objects.all().delete()
        dataset_path = os.path.join("/usr", "src", "app", "media", "docs", "Dataset")
        for file_type in os.listdir(dataset_path):
            path_to_file = os.path.join(dataset_path, file_type)
            for file in os.listdir(path_to_file):
                print(file)
                filepath = os.path.join(path_to_file, file)
                print(filepath)
                doc, created = Document.objects.get_or_create(file=filepath)
                with open(filepath, 'rb') as f:
                    doc.file.save(file, File(f), save=True)
