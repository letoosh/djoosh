# -*- coding: utf-8 -*-
from djoosh import utils

def create_index_handler(search_model, sender=None, **kwargs):
    """ Used on syncdb"""
    utils.create_index(search_model)


def update_index_handler(search_model, sender, instance, created, **kwargs):
    """ Update a record in search index, used on post_save """
    utils.update_index(search_model, instance, created)


def delete_handler(search_model, sender, instance, **kwargs):
    """ Delete a record in search index, used on pre_delete """
    utils.delete(search_model, instance, created)


