# -*- coding: utf-8 -*-
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
        mod = site.get_search_model(self.model)
        if mod:
            hits = utils.search_index(mod, query, fields)
            criteria = {'%s__in'%mod.pk: [hit[mod.pk] for hit in hits]}
            return self.model.objects.filter(**criteria)
        else:
            return self.model.objects.all()
    
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
    
    
    