from django.db import models

SOURCE_CHOICES = [
    ('pib', 'PIB'),
    ('the-hindu', 'The Hindu'),
    ('indian-express', 'The Indian Express'),
]


class Article(models.Model):
    """Replaces news.html's 10 hardcoded card divs and article.html's
    single non-dynamic detail page (its <h1> was literally the text
    "Article", not wired to any id or data source — this model and its
    detail view make that page real)."""
    title = models.CharField(max_length=250)
    summary = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, blank=True)
    icon = models.CharField(max_length=60, blank=True, help_text='Font Awesome class, e.g. "fas fa-leaf"')
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
