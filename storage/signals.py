from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import UploadedFile


@receiver(pre_save, sender=UploadedFile)
def delete_old_file_on_update(sender, instance, **kwargs):
    """
    Deletes the old file if a new file is uploaded to the model.
    """
    if not instance.pk:
        return

    try:
        old_instance = UploadedFile.objects.get(pk=instance.pk)
    except UploadedFile.DoesNotExist:
        return

    if (
        old_instance.stored_file
        and old_instance.stored_file.name != instance.stored_file.name
    ):
        old_instance.stored_file.delete(save=False)


@receiver(post_delete, sender=UploadedFile)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes the physical file from the system when the model instance is deleted.
    """
    if instance.stored_file:
        instance.stored_file.delete(save=False)
