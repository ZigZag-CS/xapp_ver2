# -*- coding: utf-8 -*-

import random
import string

from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Key pentru activarea emailului
def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key

# URL pentru activarea emailului
def unique_url_generator(instance):
    """
    This is for a Django project with an key field
    """
    key = instance.key
    url = None
    if key:
        base_url = getattr(settings, 'BASE_URL', 'https://www.pythonecommerce.com')
        key_path = reverse("account:email-activate", kwargs={'key': key})  # use reverse
        url = f"{base_url}{key_path}"
    return url



def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug