from PIL import Image
from io import BytesIO


class IMAGE:
    def __init__(self, file):
        self.image = self.get_image(file)

    @staticmethod
    def get_image(file):
        return Image.open(file)

    def convert(self):
        self.image.thumbnail((400, 400))
        bio = BytesIO()
        self.image.save(bio, format='PNG')
        return bio