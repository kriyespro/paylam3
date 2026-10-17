import json
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.prelims.models import Choice, Question

# (legacy JS variable in api.js, Question.type value)
BANKS = [
    ('pyqBank', 'pyq'),
    ('mcqBank', 'mcq'),
]


class Command(BaseCommand):
    help = 'One-time import of api.js MockDB pyqBank/mcqBank into Question/Choice rows.'

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / 'api.js'
        if not file_path.exists():
            raise CommandError('api.js not found at repo root.')

        total = 0
        for varname, q_type in BANKS:
            data = self.extract_js(file_path, varname)
            total += self.import_bank(data, q_type)

        self.stdout.write(self.style.SUCCESS(f'Imported {total} questions.'))

    def import_bank(self, data, q_type):
        count = 0
        with transaction.atomic():
            for item in data:
                question, _ = Question.objects.update_or_create(
                    external_id=item['id'],
                    defaults={
                        'type': q_type,
                        'year': item.get('year', ''),
                        'subject': item.get('subject', ''),
                        'topic': item.get('topic', ''),
                        'difficulty': item.get('difficulty', ''),
                        'est_time': item.get('estTime', ''),
                        'text': item['question'],
                        'explanation': item.get('explanation', ''),
                    },
                )
                question.choices.all().delete()
                correct_index = item.get('correctIndex')
                Choice.objects.bulk_create([
                    Choice(
                        question=question,
                        text=option_text,
                        is_correct=(idx == correct_index),
                        order=idx,
                    )
                    for idx, option_text in enumerate(item.get('options', []))
                ])
                count += 1
        return count

    def extract_js(self, file_path, varname):
        script = settings.BASE_DIR / 'scripts' / 'js_data_to_json.js'
        result = subprocess.run(
            ['node', str(script), str(file_path), varname],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise CommandError(f'node extractor failed for {varname}: {result.stderr}')
        return json.loads(result.stdout)
