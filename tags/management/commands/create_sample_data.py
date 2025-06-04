from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tags.models import Tag

class Command(BaseCommand):
    help = 'Create sample data for the STL Collection Manager'

    def handle(self, *args, **options):
        # Create sample tags
        sample_tags = [
            'Fantasy', 'Sci-Fi', 'Medieval', 'Modern', 'Vehicles', 'Characters', 
            'Buildings', 'Terrain', 'Weapons', 'Miniatures', 'Tabletop', 'D&D'
        ]

        self.stdout.write("Creating sample tags...")
        created_count = 0
        for tag_name in sample_tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                self.stdout.write(f"Created tag: {tag_name}")

        self.stdout.write(f"Created {created_count} new tags")
        self.stdout.write(f"Total tags in database: {Tag.objects.count()}")

        # Create a test superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write("Creating admin user...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(
                self.style.SUCCESS("Admin user created (username: admin, password: admin123)")
            )
        else:
            self.stdout.write("Admin user already exists")

        self.stdout.write(
            self.style.SUCCESS("\nSample data creation completed!")
        )
        self.stdout.write("You can now:")
        self.stdout.write("1. Visit the admin interface at /admin/ (username: admin, password: admin123)")
        self.stdout.write("2. Upload some STL files through the upload interface")
        self.stdout.write("3. Assign tags to your uploads")
        self.stdout.write("4. Browse the collection gallery")
