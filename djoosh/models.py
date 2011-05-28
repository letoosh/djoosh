# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from djoosh import site

for app_name in settings.INSTALLED_APPS:
    try:
        __import__('%s.search'%app_name)
    except ImportError, e:
        pass

mods = models.get_models()

for model in mods:
    try:
        if getattr(model, '_is_djoosh', False):
            site.register(model)
    except RuntimeError:
        pass

    
