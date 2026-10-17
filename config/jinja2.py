from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def attr_value(obj, attr):
    """Resolves a dotted-free attribute name for the platform_admin generic
    list template, calling it if it's a method (e.g. get_source_display)."""
    value = getattr(obj, attr)
    return value() if callable(value) else value


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'attr_value': attr_value,
    })
    return env
