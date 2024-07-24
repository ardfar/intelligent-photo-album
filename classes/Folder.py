import os

class Folder:
    def __init__(self, path):
        self.path = path

    def count_images(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        count = 0

        for root, dirs, files in os.walk(self.path):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    count += 1

        return count

    def get_images(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        images = []

        for root, dirs, files in os.walk(self.path):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    image_path = os.path.join(root, file)
                    images.append(image_path)

        return images