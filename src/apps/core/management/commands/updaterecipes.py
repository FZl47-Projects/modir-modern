from django.core.management.base import BaseCommand
from apps.restaurant.models import Recipe


class Command(BaseCommand):
    help = 'Call save method for all recipe objects'

    def handle(self, *args, **options):
        objects = Recipe.objects.all()
        for obj in objects:
            obj.save()

        self.stdout.write('Command executed successfully')
