from PIL import Image

def openImg(path):
    image = Image.open(path)
    image.show()