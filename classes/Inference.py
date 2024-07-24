from ultralytics import YOLO
import easyocr
import torch
import torchvision.transforms as transforms
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import json
import spacy

class Inference:
    def __init__(self):
        self.model = YOLO("model/coco-yolo.pt")
        # self.w2v = gensim.models.KeyedVectors.load_word2vec_format("model/GoogleNews-vectors-negative300.bin", binary=True)  
        self.threshold = 0.65
        self.ocr = easyocr.Reader(['en', "id"])

    def get_objects(self, image_path):
        detected_objects = []
        try:
            results = self.model.predict(image_path, verbose=False)
            filtered_results = [result for result in results if any(box.conf > self.threshold for box in result.boxes)]

            for result in filtered_results:
                for box in result.boxes:
                    class_id = int(box.cls)
                    class_name = self.model.names[class_id]
                    detected_objects.append(class_name)
        except (IOError, OSError, ValueError):
            # Skip the unreadable image
            pass
        return json.dumps(detected_objects)
    
    def get_text(self, image_path):
        try:
            result = self.ocr.readtext(image_path, detail=0, decoder='greedy', min_size=10)
            result_str = ' '.join(result)
            return result_str
        except (IOError, OSError, ValueError):
            # Skip the unreadable image
            pass
        return None
        
    def get_scene(self, image_path, target_size=(512, 512)):  # Adjust target_size and class_names if needed

        model = torch.load('model/scene-classifier.pth')
        model.to('cuda')
        
        classnames = ['architecture','art','document','foods','group photo','landscape','natural','potrait','sky','transport','waterfront']

        # Load the image using PIL or OpenCV
          # Assuming PIL for simplicity
        image = Image.open(image_path)
        
        # Convert RGBA image to RGB if the image is RGBA
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Preprocess the image
        transform = transforms.Compose([
            transforms.Resize(target_size),  # Adjust resize dimensions if your model expects a different size
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))  # Adjust normalization parameters if needed
        ])
        preprocessed_image = transform(image)

        # Add a batch dimension (if the model expects batches)
        preprocessed_image = preprocessed_image.unsqueeze(0)

        # Move the image to the device (CPU or GPU)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        preprocessed_image = preprocessed_image.to(device)

        # Perform inference
        with torch.no_grad():
            outputs = model(preprocessed_image)

        # Get the predicted class index (highest probability)
        _, predicted_class_idx = torch.max(outputs.data, 1)

        # Get the predicted class probability
        predicted_class_prob = torch.softmax(outputs.data, dim=1)[0][predicted_class_idx.item()]

        # Set the accuracy threshold
        accuracy_threshold = 0.25

        # Check if the predicted class probability is above the threshold
        if predicted_class_prob > accuracy_threshold:
            # Optionally, map the class index to a class name using class_names list
            predicted_class_name = classnames[predicted_class_idx.item()]
        else:
            predicted_class_name = "Unknown"

        return predicted_class_name
    
    def get_caption(self, image_path):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda") 
        raw_image = Image.open(image_path).convert('RGB')

        # conditional image captioning
        text = "a photography of"
        inputs = processor(raw_image, text, return_tensors="pt").to("cuda")

        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    
    def get_entities(self, sentence):
        entities = []
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(sentence)
        objects = [token.text for token in doc if token.pos_ in ['NOUN', 'PRON']]
        return objects
    
    # def get_similar_words(self, word):
    #     try:
    #         similar_words = self.w2v.most_similar(word, topn=5)
    #         return [word for word, similarity in similar_words]
    #     except KeyError:
    #         return f"The word '{word}' is not in the vocabulary."
    
    def clear_cache(self):
        torch.cuda.empty_cache()