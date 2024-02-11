from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.oid = instance.id + 100
        instance.save()
