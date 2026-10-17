from datetime import date

from django.core.management.base import BaseCommand

from apps.current_affairs.models import Article

# Transcribed verbatim from news.html's 10 hardcoded <div class="news-card">
# entries (title, source, category, icon, body) — the legacy site's own
# existing copy, not invented content. The legacy cards carried no real
# publish date (static demo markup), so all rows use today's date at import
# time rather than fabricating a history that never existed.
ARTICLES = [
    ('pib', 'Education', 'fas fa-building',
     "Government launches new initiative for digital education",
     "The Ministry of Education has announced a comprehensive plan to integrate digital learning tools in rural schools across the country."),
    ('the-hindu', 'UPSC Update', 'fas fa-university',
     "UPSC Prelims 2026: Expected changes in exam pattern",
     "Experts weigh in on the potential shift towards more analytical questions in the upcoming Civil Services Preliminary Examination."),
    ('indian-express', 'Economy', 'fas fa-chart-line',
     "RBI announces new monetary policy review",
     "The Reserve Bank of India has maintained the repo rate, prioritizing inflation control amidst global economic uncertainties."),
    ('pib', 'Environment', 'fas fa-leaf',
     "India achieves renewable energy target ahead of schedule",
     "A major milestone in climate action as India crosses the 200GW mark in installed non-fossil fuel capacity."),
    ('the-hindu', 'Int. Relations', 'fas fa-globe',
     "G20 Summit concludes with joint declaration on climate",
     "Member nations agree on a unified framework for technology transfer and green finance to developing nations."),
    ('pib', 'Science & Tech', 'fas fa-rocket',
     "ISRO successfully launches new earth observation satellite",
     "The latest EOS mission will significantly enhance agricultural monitoring and disaster management capabilities."),
    ('the-hindu', 'Polity', 'fas fa-gavel',
     "Supreme Court issues new guidelines on bail provisions",
     "A landmark judgment aiming to decongest prisons and uphold the principle of 'bail is rule, jail is exception'."),
    ('indian-express', 'Social Issues', 'fas fa-users',
     "National report highlights improved gender parity in higher education",
     "Recent survey data indicates a significant narrowing of the gender gap in STEM enrollments across state universities."),
    ('the-hindu', 'Geography', 'fas fa-cloud-sun-rain',
     "New monsoon pattern observed over the Indian subcontinent",
     "Meteorological department notes shifting rainfall trends, likely linked to broader climate change phenomena."),
    ('pib', 'UPSC Update', 'fas fa-award',
     "Final results for Civil Services Examination 2025 declared",
     "The Commission has released the final merit list, with women candidates securing top positions again this year."),
]


class Command(BaseCommand):
    help = 'One-time import of news.html\'s 10 hardcoded article cards into Article rows.'

    def handle(self, *args, **options):
        today = date.today()
        count = 0
        for source, category, icon, title, summary in ARTICLES:
            Article.objects.update_or_create(
                title=title,
                defaults={
                    'source': source,
                    'category': category,
                    'icon': icon,
                    'summary': summary,
                    'published_date': today,
                },
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {count} articles.'))
