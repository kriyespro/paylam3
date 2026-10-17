import json
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.mains.models import MainsQuestion


class Command(BaseCommand):
    help = 'One-time import of mains-pyq-data.js mainsPYQData into MainsQuestion rows.'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'mains-pyq-data.js'
        if not file_path.exists():
            raise CommandError('mains-pyq-data.js not found at repo root.')

        data = self.extract_js(file_path, 'mainsPYQData')

        count = 0
        for item in data:
            MainsQuestion.objects.update_or_create(
                external_id=str(item['id']),
                defaults={
                    'paper': item['paper'],
                    'year': item['year'],
                    'subject': item.get('subject', ''),
                    'marks': item['marks'],
                    'text': item['question'],
                    'model_answer': item.get('modelAnswer', {}),
                },
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {count} mains questions.'))

    def extract_js(self, file_path, varname):
        script = settings.BASE_DIR / 'scripts' / 'js_data_to_json.js'
        result = subprocess.run(
            ['node', str(script), str(file_path), varname],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise CommandError(f'node extractor failed: {result.stderr}')
        return json.loads(result.stdout)
