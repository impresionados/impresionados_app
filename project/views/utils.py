import os

def get_images():
    images = []
    for filename in os.listdir("../imagens"):
        if filename.endswith(".jpeg") or filename.endswith(".jpg"):
            images.append(os.path.join("../imagens", filename))
    return images
