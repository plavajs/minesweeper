import os

__scriptDir = os.path.dirname(os.path.realpath(__file__))


def get_image_path(imageName: str):
    imagePath = os.path.join(__scriptDir, "images", imageName)
    return imagePath.__str__().replace("\\", "/")
