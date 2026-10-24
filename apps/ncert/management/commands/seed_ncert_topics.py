from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import Subject
from apps.ncert.models import Topic

# Lifted verbatim from the legacy ncert-module.html prototype's hardcoded
# `databaseMap` — the fixed 12-subject NCERT topic taxonomy. Keyed by the
# apps.content.Subject slug each subject name maps to (see
# apps.content.management.commands.import_subjects for the slug list;
# 'science-tech' has no data.js yet, so its Subject row is created here).
SUBJECT_TOPICS = {
    'history': [
        'Pre-Historic Time', 'Indus Valley Civilization', 'Vedic Age', 'Mahajanapadas', 'Mauryan Empire',
        'Post-Mauryan Period', 'Gupta Empire', 'Harsha Empire', 'Sangam Age', 'South Indian Kingdoms',
        'Ancient Religions', 'Ancient Art & Architecture', 'Palas', 'Pratiharas', 'Rashtrakutas',
        'Delhi Sultanate', 'Vijayanagara Empire', 'Bahmani Kingdom', 'Mughal Empire', 'Marathas',
        'Bhakti Movement', 'Sufi Movement', 'Medieval Architecture', 'Advent of Europeans',
        'Consolidation of British Power', 'Revolt of 1857', 'Social & Religious Reforms', 'INC Formation',
        'Gandhian Era', 'Revolutionary Movement', 'Constitutional Development', 'Partition & Independence',
        'Introduction', 'Art & Architecture', 'Temple Architecture', 'Cave Architecture', 'Paintings',
        'Sculpture', 'Music', 'Dance', 'Theatre', 'Puppetry', 'UNESCO Heritage', 'Festivals', 'Literature',
        'Religion & Philosophy', 'Handicrafts', 'Industrial Revolution', 'French Revolution',
        'American Revolution', 'Russian Revolution', 'Unification of Germany', 'Unification of Italy',
        'World War I', 'World War II', 'Cold War', 'Decolonization',
    ],
    'geography': [
        'Physical Setting of India', 'Major Physical Division of India', 'Drainage System', 'Indian Climate',
        'Indian Monsoon', 'Indian Soils', 'Land Resource in India', 'Mineral Resource', 'Energy Resources',
        'Forest', 'Agriculture', 'Manufacturing and Services', 'Transport', 'Communication',
        'Hazards and Disasters', 'Population and Settlement', 'Universe: Origin and Evolution',
        'Movement of Earth', "Earth's Internal Structure", 'Tectonics', 'Rocks', 'Landforms', 'Soil',
        'Atmosphere', 'Hydrological Cycle', 'Weather Phenomenon', 'Ocean', 'Climate Regions of The world',
        'Oceans', 'Continents', 'World Economic Geography', 'World Human Geography',
    ],
    'polity': [
        'Historical Background', 'Concept and Salient Features of the Constitution', 'Preamble of the Constitution',
        'Union and Its Territory', 'Citizenship', 'Fundamental Rights', 'Directive Principles of State Policy',
        'Fundamental Duties', 'Union Executive', 'Parliament', 'Parliamentary Committees', 'State Executive',
        'State Legislature', 'Union Territories and Special Areas', 'Supreme Court', 'High Court',
        'Subordinate Courts', 'Alternative Dispute Resolution Courts', 'Tribunals', 'Judicial Review',
        'Basic Structure', 'Basics of Federal System', 'Centre-State Relations', 'Inter-State Relations',
        'Panchayati Raj', 'Urban Local Bodies', 'Elections', 'Political Dynamics', 'Emergency Provisions',
        'Amendment of the Constitution', 'Other Constitutional Dimensions', 'Constitutional Bodies',
        'Non-Constitutional Bodies', 'Constituents of Indian Constitution', 'Laws and Legislations',
    ],
    'economy': [
        'Introduction to Economics', 'National Income Accounting', 'Money, Banking and Monetary Policy',
        'Finance and Financial Markets', 'Public Finance in India', 'Taxation in India', 'Inflation',
        'Unemployment', 'Poverty', 'Agriculture and Allied Activities', 'Food Processing',
        'Industry and Manufacturing', 'Infrastructure and Investment Models in India',
        'Services and Digital Economy', 'Trade and External Sector', 'Planning and Reform',
        'International Institutions', 'Sustainable and Inclusive Growth',
    ],
    'environment': [
        'Ecology', 'Functions of Ecosystem', 'Terrestrial Ecosystem', 'Aquatic Ecosystem', 'Wet Land Ecosystem',
        'Environmental Pollution', 'Renewable Energy', 'Environmental Impact Assessment (EIA)',
        'Biodiversity Basics', 'Indian Biodiversity – Diverse Landscape', 'Schedule Animals of WPA 1972',
        'Animal Diversity of India', 'Plant Diversity of India', 'Marine Organisms', 'Protected Area Network',
        'Conservation Efforts', 'Climate Change', 'Ocean Acidification', 'Ozone Depletion',
        'Impact of Climate Change', 'Mitigation Strategies',
    ],
    'science-tech': [
        'Space Technology', 'Biotechnology', 'Information Technology', 'Nanotechnology', 'Defense Technology',
        'Health and Diseases', 'Energy Sector', 'Robotics and AI',
    ],
    'social-issue': [
        'Related to Vulnerable Sections', 'Related to Human Development and Dignity',
        'Related to Society and Its Fabric', 'Types of Schemes', 'Agriculture and Allied Sector',
        'Economy and Finance', 'Environment', 'Governance', 'Health and Welfare', 'Human Development',
        'Industry and Energy', 'Infrastructure and Communication', 'Science and Technology',
    ],
    'ir': [
        'Basics of International Relations', "Evolution of India's Foreign Policy",
        'Events and Developments in Foreign Nations', 'India and its Neighbourhood Relations',
        'India and Africa Relations', 'India and Central Asia Relations', 'India and Europe Relations',
        'India and Indo-Pacific Relations', 'India and South East Asia Relations',
        'India and West Asia Relations', 'India and Latin America-Caribbean Relations',
        'India and Russia Relations', 'India and USA Relations', 'Relations with Other Countries',
        'The United Nations', 'Multilateral Groupings', 'Regional Groupings', 'Indian Diaspora',
    ],
    'governance': [
        'Governance: Concepts and Framework', 'Transparency and Accountability',
        'Development Processes and Stakeholders', 'Pressure Groups and Civil Society',
        'Role of Civil Services in a Democracy',
    ],
    'disaster-management': [
        'Foundations of Disaster Management', 'Specific Disasters and Hazard-wise Management',
        'Institutional and Legal Framework', 'Enabling Mechanisms in Disaster Management',
    ],
    'internal-security': [
        'Internal Security Challenges', 'Insurgency, Radicalisation and Terrorism',
        'External and Border Threats', 'Cybercrime and Information Security',
        'Economic and Financial Security', 'Security Forces and Intelligence',
    ],
    'ethics': [
        'Introduction to Ethics and Moral Philosophy', 'Ethics and Human Interface',
        'Human Values and Socialisation', 'Attitude and Behaviour', 'Emotional Intelligence',
        'Foundational Values for Civil Services', 'Aptitude and Civil Service Ethics',
        'Ethics in Public Administration and Governance', 'Probity in Governance',
        'Corporate and Economic Ethics', 'Thinkers and Philosophical Foundations',
        'Case Studies and Ethical Application Frameworks',
    ],
}


class Command(BaseCommand):
    help = 'Seeds the fixed NCERT subject/topic taxonomy (from the legacy ncert-module.html prototype) as real Topic rows.'

    @transaction.atomic
    def handle(self, *args, **options):
        # science-tech has no *-data.js yet (see import_subjects), so it has
        # no Subject row — create a minimal placeholder so NCERT topics
        # have somewhere to live rather than skipping the subject entirely.
        science_tech, created = Subject.objects.get_or_create(
            slug='science-tech',
            defaults={
                'name': 'Science & Tech', 'icon': 'fas fa-microscope', 'theme': 'green',
                'tagline': 'Space, biotech, IT, and defense technology for the UPSC syllabus.',
                'order': 11,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created placeholder Subject: science-tech'))

        total_topics = 0
        for slug, topics in SUBJECT_TOPICS.items():
            try:
                subject = Subject.objects.get(slug=slug)
            except Subject.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'No Subject with slug "{slug}" — skipping its topics. Run import_subjects first.'))
                continue

            for order, name in enumerate(topics):
                _, created = Topic.objects.get_or_create(subject=subject, name=name, defaults={'order': order})
                total_topics += 1 if created else 0

        self.stdout.write(self.style.SUCCESS(f'Seeded {total_topics} new NCERT topics across {len(SUBJECT_TOPICS)} subjects.'))
