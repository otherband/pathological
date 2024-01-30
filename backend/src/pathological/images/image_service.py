from pathological import resources_utils


class ImageService:
    def get_image_by_id(self, image_id):
        return resources_utils.resource_path(image_id)
