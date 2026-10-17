from django.db import migrations

PLANS = [
    {
        'slug': 'starter',
        'name': 'Starter',
        'price_inr': 999,
        'duration_days': 90,
        'is_popular': False,
        'order': 1,
        'features': [
            'Subject-wise basic courses',
            'Practice Questions',
            'Limited Tests',
            '3 Months Access',
        ],
    },
    {
        'slug': 'pro',
        'name': 'Pro',
        'price_inr': 2999,
        'duration_days': 180,
        'is_popular': True,
        'order': 2,
        'features': [
            'All Important Subjects',
            'Prelims Preparation',
            'MCQ Practice',
            'Mock Tests',
            'Current Affairs',
            '6 Months Access',
        ],
    },
    {
        'slug': 'premium',
        'name': 'Premium',
        'price_inr': 5999,
        'duration_days': 365,
        'is_popular': False,
        'order': 3,
        'features': [
            'Complete Prelims + Mains',
            'All Subjects',
            'PYQs',
            'Mock Tests',
            'Mains Answer Writing',
            'Model Answers',
            'Performance Analytics',
            '12 Months Access',
        ],
    },
]


def seed_plans(apps, schema_editor):
    Plan = apps.get_model('billing', 'Plan')
    for data in PLANS:
        Plan.objects.update_or_create(slug=data['slug'], defaults=data)


def unseed_plans(apps, schema_editor):
    Plan = apps.get_model('billing', 'Plan')
    Plan.objects.filter(slug__in=[p['slug'] for p in PLANS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_plans, unseed_plans),
    ]
