# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.functional import curry
from django.db.models import signals
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from djoosh.signals import create_index_handler, update_index_handler, delete_handler
import os

class Site(object):
    _models = {}
    _schemas = {}
    
    def __init__(self, **models):
        for key in models:
            self._models[key] = models[key]
    
    def register(self, model, search_model=None):
        
        if not search_model:
            search_model = SearchModel(model)
            
        model_key = "%s.%s" % (model._meta.app_label, model.__name__)
        
        if model_key in self._schemas or model_key in self._models:
            raise RuntimeError('%s is already registered.' % model.__name__)
        
        if not search_model.model:
            search_model.model = model
            
        self._models[model_key] = search_model
        self._schemas[model_key] = search_model.schema
        
        search_model.signal_syncdb = curry(create_index_handler, search_model=search_model)
        search_model.signal_update = curry(update_index_handler, search_model=search_model)
        search_model.signal_delete = curry(delete_handler, search_model=search_model)
        
        signals.post_syncdb.connect(search_model.signal_syncdb, sender=model)
        signals.post_save.connect(search_model.signal_update, sender=model)
        signals.pre_delete.connect(search_model.signal_delete, sender=model)
    
    def get_models(self):
        return self._models.values()
    
    def get_search_model(self, model):
        model_key = "%s.%s" % (model._meta.app_label, model.__name__)
        return self._models.get(model_key, None)
    
    def unregister(self, model):
        
        model_key = "%s.%s" % (model._meta.app_label, model.__name__)
        
        if model_key in self._schemas:
            del self._schemas[model_key]
            
        if model_key in self._models:
            del self._models[model_key]


class SearchModel(object):
    pk = 'id'
    fields = []
    exclude = []
    stored = []
    keywords = []
    schema = None
    model = None
    
    def __init__(self, model=None):
        if model:
            self.fields = model._meta.get_all_field_names()
            self.model = model
            
        self.fields = set(self.fields) - set(self.exclude)
        schema_options = {}
        
        for field in self.fields:
            if field == self.pk:
                schema_options[field] = ID(stored=True, unique=True)
            elif field in self.keywords:
                schema_options[field] = KEYWORD(stored=field in self.stored)
            else:
                schema_options[field] = TEXT(stored=field in self.stored)
        self.schema = Schema(**schema_options)
    
    def get_name(self):
        return "%s.%s" % (self.model._meta.app_label, self.model.__name__)
    
    def get_path(self):
        return os.path.join(settings.DJOOSH_INDEX, self.get_name())

site = Site()
