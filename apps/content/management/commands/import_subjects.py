import json
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.content.models import Lesson, Module, Subject, Unit

# (slug, display name, legacy data file, legacy JS variable name, theme)
# Matches the 11 subject-*.html pages that have a real *-data.js today.
# subject-science-tech.html has no data file yet (still a placeholder stub) —
# deliberately excluded here, not a bug.
# Theme matches each legacy page's own --premium-primary (checked via grep
# across all 11 subject-*.html files, not assumed uniform).
SUBJECTS = [
    ('polity', 'Indian Polity', 'polity-data.js', 'polityDatabase', 'green',
     'Premium Learning Module. Master Indian constitution, governance, rights, and legislative processes with structured units.'),
    ('history', 'History & Culture', 'history-data.js', 'historyDatabase', 'navy',
     'Premium Learning Module. Master ancient to modern history with structured units and practice tests.'),
    ('geography', 'Geography', 'geography-data.js', 'geographyDatabase', 'navy',
     'Premium Learning Module. Master Indian, Physical, and World Geography with structured units and practice tests.'),
    ('economy', 'Economics', 'economy-data.js', 'economyDatabase', 'green',
     'Premium Learning Module. Master national income, banking, taxation, and economic reforms with structured units.'),
    ('environment', 'Environment & Ecology', 'environment-data.js', 'environmentDatabase', 'green',
     'Premium Learning Module. Master ecology, biodiversity, climate change, and environmental laws with structured units.'),
    ('governance', 'Governance', 'governance-data.js', 'governanceDatabase', 'green',
     'Premium Learning Module. Master governance concepts, transparency, development processes, and civil services with structured units.'),
    ('ir', 'International Relations', 'ir-data.js', 'irDatabase', 'green',
     'Premium Learning Module. Master foreign policy, international events, and bilateral relations with structured units.'),
    ('internal-security', 'Internal Security', 'internal-security-data.js', 'internalSecurityDatabase', 'green',
     'Premium Learning Module. Master internal security challenges, cybercrime, border threats, and intelligence with structured units.'),
    ('disaster-management', 'Disaster Management', 'disaster-management-data.js', 'disasterDatabase', 'orange',
     'Premium Learning Module. Master foundations, hazards, and institutional frameworks with structured units.'),
    ('ethics', 'Ethics', 'ethics-data.js', 'ethicsDatabase', 'green',
     'Premium Learning Module. Master moral philosophy, human values, and public administration ethics with structured units.'),
    ('social-issue', 'Social Issues & Schemes', 'social-issue-data.js', 'socialIssueDatabase', 'green',
     'Premium Learning Module. Master social fabric, human development, and government schemes with structured units.'),
]


class Command(BaseCommand):
    help = 'One-time import of the legacy *-data.js subject content into Subject/Module/Unit/Lesson rows.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--slug', help='Only import this one subject slug (default: all 11).', default=None,
        )

    def handle(self, *args, **options):
        only_slug = options.get('slug')
        targets = [s for s in SUBJECTS if only_slug is None or s[0] == only_slug]
        if not targets:
            raise CommandError(f'No known subject with slug "{only_slug}"')

        for order, (slug, name, filename, varname, theme, tagline) in enumerate(targets):
            self.import_one(order, slug, name, filename, varname, theme, tagline)

    def import_one(self, order, slug, name, filename, varname, theme, tagline):
        file_path = settings.BASE_DIR / filename
        if not file_path.exists():
            raise CommandError(f'{filename} not found at repo root — expected legacy data file.')

        data = self.extract_js(file_path, varname)

        with transaction.atomic():
            subject, _ = Subject.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name, 'icon': data[0]['icon'] if data else '',
                    'theme': theme, 'tagline': tagline, 'order': order,
                },
            )

            for mod_order, mod in enumerate(data):
                module, _ = Module.objects.update_or_create(
                    subject=subject,
                    key=mod['id'],
                    defaults={'title': mod['title'], 'icon': mod.get('icon', ''), 'order': mod_order},
                )

                for unit_order, unit in enumerate(mod['units']):
                    unit_obj, _ = Unit.objects.update_or_create(
                        module=module,
                        key=unit['id'],
                        defaults={'title': unit['title'], 'order': unit_order},
                    )

                    unit_obj.lessons.all().delete()
                    Lesson.objects.bulk_create([
                        Lesson(
                            unit=unit_obj,
                            title=lesson['title'],
                            type=lesson.get('type', 'text'),
                            duration=lesson.get('duration', ''),
                            description=lesson.get('description', ''),
                            order=lesson_order,
                        )
                        for lesson_order, lesson in enumerate(unit['lessons'])
                    ])

        self.stdout.write(self.style.SUCCESS(f'Imported {slug}: {len(data)} modules'))

    def extract_js(self, file_path, varname):
        script = settings.BASE_DIR / 'scripts' / 'js_data_to_json.js'
        result = subprocess.run(
            ['node', str(script), str(file_path), varname],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise CommandError(f'node extractor failed for {file_path}: {result.stderr}')
        return json.loads(result.stdout)
