from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    """
    Replaces blogs.html, which was (and still is, in the legacy static
    site) a literal "Coming Soon" placeholder with zero real posts. No seed
    content here on purpose — same call as subject-science-tech.html in
    Phase 3: there's nothing real to port, only a stub. This model is ready
    for real posts via admin; it doesn't fabricate any to look finished.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
