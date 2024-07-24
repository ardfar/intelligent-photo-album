import json
import os
import classes.Index as Index


class Photo:
    def __init__(self, path):
        self.path = path
        self.objects = []
        self.text = None
        self.caption = ""
        self.class_name = None
        self.index = Index.Index()
        
    def load_image_from_index(self):
        data = self.index.get_image(self.path)
        
        self.objects = data[3]
        self.class_name = data[4]
        self.text = data[5]
        self.caption = data[6]
        
    def set_caption(self, caption):
        self.caption = caption
        
    def set_objects(self, objects):
        self.objects = objects
        
    def get_objects(self):
        return self.objects
    
    def set_text(self, text):
        self.text = text
    
    def get_text(self):
        return self.text
    
    def set_class(self, class_name):
        self.class_name = class_name
        
    def get_class(self):
        return self.class_name
        
    def save(self):
        self.index.add_index(
            os.path.basename(self.path), 
            self.path, 
            self.objects, 
            self.class_name, 
            self.text,
            self.caption
            )