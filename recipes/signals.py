import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe  # Why?


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


# I think.. if delete could cause errors, this code would be problematic, as it would delete the cover before the recipe instance was deleted
@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()  # This line of code is prob useless in this scenario

    if old_instance:
        delete_cover(old_instance)


# Luiz Otavio acknowledging the old file should only be deleted on post_save, does it on pre_save anyway
@receiver(pre_save, sender=Recipe)
def recipe_cover_delete_signal(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
