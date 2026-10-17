from django.db import models

THEME_CHOICES = [
    ('green', 'Green'),
    ('navy', 'Navy & Gold'),
    ('orange', 'Orange'),
]

LESSON_TYPE_CHOICES = [
    ('text', 'Text'),
    ('video', 'Video'),
    ('practice', 'Practice'),
    ('quiz', 'Quiz'),
    ('pdf', 'PDF'),
]


class Subject(models.Model):
    """One of the 11 (soon 12) top-level subjects — was a `subject-*.html` page
    paired with a `*-data.js`/`*-ui.js` file. `slug` matches the old page's
    name suffix (e.g. 'polity' for subject-polity.html)."""
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=60, blank=True, help_text='Font Awesome class, e.g. "fas fa-gavel"')
    theme = models.CharField(
        max_length=10, choices=THEME_CHOICES, default='green',
        help_text='Matches the legacy subject page\'s --premium-primary theme (9 of 11 subjects used green; geography/history used navy, disaster-management used orange).',
    )
    tagline = models.CharField(max_length=200, blank=True, help_text="The legacy premium-header's <p> description text.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Module(models.Model):
    """A subject page's top-level cards — almost always exactly two per
    subject in the legacy data: the main syllabus and a 'Final Revision'
    block. Kept as its own level rather than folded into Subject because the
    legacy data genuinely has this extra layer."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='modules')
    key = models.SlugField(help_text="Original JS id, e.g. 'final-revision-section'")
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=60, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = [('subject', 'key')]

    def __str__(self):
        return f'{self.subject.slug} / {self.title}'


class Unit(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='units')
    key = models.CharField(max_length=60, help_text="Original JS id, e.g. 'p-unit-1'")
    title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = [('module', 'key')]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Content only — no per-user completion flag here. The legacy data.js had
    a hardcoded `completed: false` on every lesson (never actually toggled
    anywhere in the codebase), which is user progress state, not content.
    That belongs in apps.engagement against a real user once Phase 8 builds
    it; duplicating it here would just be a second, unsynced copy.
    """
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='text')
    duration = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
