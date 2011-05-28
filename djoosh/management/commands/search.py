# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings 
from djoosh import site
from djoosh.utils import create_index, update_index

class Command(BaseCommand):
    args = '<command>'
    help = """
    Manage the search index.
    
    Available commands:
    
        rebuild - Rebuild search index for all existing models
    """
    
    def handle(self, *args, **options):
        try:
            command = args[0]
        except:
            raise CommandError('Please provide a valid command')
        
        if command == 'rebuild':
            for model in site.get_models():
                self.stdout.write('Creating index for %s... ' % model.get_name())
                create_index(model)
                update_index(model)
                self.stdout.write('DONE\n')
        
        