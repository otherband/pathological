from pathological.resources_utils import resource_path

READ_BYTES = "rb"


class ImageService:
    def get_image_by_id(self, image_id):
        with open(resource_path(image_id), READ_BYTES) as file:
            return file.read()
