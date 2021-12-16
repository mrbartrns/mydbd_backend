from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from io import BytesIO
from PIL import Image as PILImage
from .models import Comment, Image


@receiver(post_save, sender=Comment)
def check_comment_depth(sender, instance, created, **kwargs):
    if created and instance.parent:
        # instance.depth = instance.parent.depth + 1
        instance.depth = 1
        instance.save()


@receiver(pre_save, sender=Image)
def resize_image(sender, instance, **kwargs):
    resize_width = 780

    image = PILImage.open(instance.image)
    fmt = image.format
    if fmt == "gif":
        return
    image_width, image_height = image.size

    width = 0
    height = 0

    # resize only when image width is over resize_width
    if image_width > resize_width:
        width = resize_width
        height = (image_height * resize_width) // image_width
    # resize image
    image = image.resize((width, height), PILImage.ANTIALIAS)

    # 메모리 상에서 byte 데이터를 처리하는 BytesIO 클래스 사용
    buffer = BytesIO()
    image.save(buffer, format="png")

    file = InMemoryUploadedFile(
        buffer,
        "{}".format(instance.image),
        "{}".format(instance.image),
        "image/png",
        buffer.tell(),
        None,
    )
    instance.image = file


# @receiver(post_save, sender=Comment)
# def set_comment_sequence(sender, instance, created, **kwargs):
#     if created and instance.parent:
#         seq = instance.parent.children.order_by("-seq").first().seq
#         instance.seq = seq + 1
#         instance.save()


# @receiver(post_save, sender=Comment)
# def set_group(sender, instance, created, **kwargs):
#     if created:
#         group = instance.id
#         if instance.parent:
#             group = instance.parent.group
#         instance.group = group
#         instance.save()
