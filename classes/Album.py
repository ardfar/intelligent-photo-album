import json
import os
import random
import classes.Index as Index


class Album:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.members = []
        self.thumbnail = None
        self.indexer = Index.Index()
        
    def get_name(self):
        
        if self.type == 'folder':
            return self.name.split(os.sep)[-1]
        
        return self.name
        
    def get_members(self):
        if self.type == 'object':
            self.members = self.indexer.get_object_members(self.name)
        elif self.type == 'folder':
            self.members = self.indexer.get_folder_members(self.name)
        else:
            self.members = self.indexer.get_type_members(self.name)
        
        self.set_thumbnail()
            
    def set_thumbnail(self):
        
        if self.members:
            self.thumbnail = self.members[random.randint(0, len(self.members)-1)][1]
            
    def get_thumbnail(self):
        return self.thumbnail