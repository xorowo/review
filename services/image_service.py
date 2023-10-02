from PIL import Image

def get(name):
    full_path = "resources/images/" + name
    return Image.open(full_path)