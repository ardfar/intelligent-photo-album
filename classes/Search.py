import classes.Inference as Inference
import classes.Index as Index


class Search:
    def __init__(self, query):
        self.query = query
        self.index = Index.Index()
        self.infer = Inference.Inference()
        
        if len(self.query.split(" ")) > 1:
            self.entities = self.infer.get_entities(self.query)
        else:
            self.entities = [self.query]
            
        self.items = {
            "person": 0, "bicycle": 1, "car": 2, "motorcycle": 3, "airplane": 4, "bus": 5,
            "train": 6, "truck": 7, "boat": 8, "traffic light": 9, "fire hydrant": 10, 
            "stop sign": 11, "parking meter": 12, "bench": 13, "bird": 14, "cat": 15, 
            "dog": 16, "horse": 17, "sheep": 18, "cow": 19, "elephant": 20, "bear": 21, 
            "zebra": 22, "giraffe": 23, "backpack": 24, "umbrella": 25, "handbag": 26, 
            "tie": 27, "suitcase": 28, "frisbee": 29, "skis": 30, "snowboard": 31, 
            "sports ball": 32, "kite": 33, "baseball bat": 34, "baseball glove": 35, 
            "skateboard": 36, "surfboard": 37, "tennis racket": 38, "bottle": 39, 
            "wine glass": 40, "cup": 41, "fork": 42, "knife": 43, "spoon": 44, "bowl": 45, 
            "banana": 46, "apple": 47, "sandwich": 48, "orange": 49, "broccoli": 50, 
            "carrot": 51, "hot dog": 52, "pizza": 53, "donut": 54, "cake": 55, 
            "chair": 56, "couch": 57, "potted plant": 58, "bed": 59, "dining table": 60, 
            "toilet": 61, "tv": 62, "laptop": 63, "mouse": 64, "remote": 65, "keyboard": 66, 
            "cell phone": 67, "microwave": 68, "oven": 69, "toaster": 70, "sink": 71, 
            "refrigerator": 72, "book": 73, "clock": 74, "vase": 75, "scissors": 76, 
            "teddy bear": 77, "hair drier": 78, "toothbrush": 79
        }
        
        self.categories = {
            'architecture': [],
            'art': [],
            'document': [],
            'foods': [46, 47, 48, 49, 50, 51, 52, 53, 54, 55],
            'group photo': [0, 13, 24, 25, 26, 27, 28, 73],
            'landscape': [],
            'natural': [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 58],
            'portrait': [0],
            'sky': [4, 33],
            'transport': [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12],
            'waterfront': [8]
        }
        self.item_to_index = {item: index for item, index in self.items.items()}
        self.index_to_category = {}
        
        for category, indices in self.categories.items():
            for index in indices:
                self.index_to_category[index] = category
        
    def get_members(self):
        
        print(self.query)
        print(self.entities)
        
        related_types = []
        rObject = []
        rType = []
        rText = self.get_photo_o_ocr(self.query)
        
        for entity in self.entities:
            
            if self.categorize_item(entity) != "None":
                related_types.append(self.categorize_item(entity))
            
            rObject += self.get_photo_o_object(entity)
            # rObject += self.get_photo_o_object(self.infer.get_similar_words(entity)[0])
            rType += self.get_photo_o_type(entity)
            # rType += self.get_photo_o_type(self.infer.get_similar_words(entity)[0])
            
        for type in related_types:
            rType += self.get_photo_o_type(type)
            
        result = {
            "rObject": rObject,
            "rType": rType,
            "rScan": rText
        }
        
        return result
        

    def get_photo_o_type(self, type):
        result = self.index.get_type_members(type)
        
        return result
    
    def get_photo_o_object(self, object):
        result = self.index.get_object_members(object)
        
        return result
    
    def get_photo_o_ocr(self, text):
        result = self.index.get_ocr_members(text)
        
        return result
    
    def categorize_item(self,item_name):
        index = self.item_to_index.get(item_name.lower())
        if index is None:
            return "Item not found"
        return self.index_to_category.get(index, "None")