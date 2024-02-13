from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django_q.models import Schedule


class Command(BaseCommand):
    help = 'Create django-q tasks'

    def handle(self, *args, **options):
        current_time = datetime.now()

        # Set next_run time
        next_run = current_time.replace(hour=1, minute=0)
        if next_run <= current_time:
            next_run += timedelta(days=1)

        # Create task to disable subscriptions
        Schedule.objects.create(
            name='Disable subscriptions',
            func='apps.core.tasks.deactivate_subs',
            schedule_type=Schedule.DAILY,
            next_run=next_run
        )

        next_run += timedelta(hours=1)

        # Create task to send subscription end warning
        Schedule.objects.create(
            name='Warn user subscription',
            func='apps.core.tasks.notif_remain_days',
            schedule_type=Schedule.DAILY,
            next_run=next_run
        )

        self.stdout.write('Create tasks command executed successfully')
