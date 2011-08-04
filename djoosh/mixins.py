# -*- coding: utf-8 -*-
from django.db.models import Q
from djoosh.utils import search_index
from djoosh import site, utils

class ClassProperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class Searcher(object):
    
    model = None
    
    def __init__(self, model):
        self.model = model
    
    def query(self, query, fields=[]):
        q = self.get_models_query(query, fields)
        return self.model.objects.filter(q)
    
    def get_models_query(self, query, fields=[], limit=None):
        mod = site.get_search_model(self.model)
        if mod:
            try:
                hits = utils.search_index(mod, query, fields, limit)
            except:
                hits = []
            criteria = {'%s__in'%mod.pk: [hit[mod.pk] for hit in hits]}
            return Q(**criteria)
        else:
            return Q()
    
    def rebuild(self):
        mod = site.get_search_model(self.model)
        if mod:
            utils.create_index(mod)
            utils.update_index(mod)
        


class SearchMixin(object):
    
    _is_djoosh = True
    
    @ClassProperty
    @classmethod
    def search(cls):
        return Searcher(cls)
    
    
    
