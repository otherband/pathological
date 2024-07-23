from abc import ABCMeta, abstractmethod

from pathological.resources_utils import resource_path

READ_BYTES = "rb"


class ImageIdToImagePathConvertor(metaclass=ABCMeta):
    @abstractmethod
    def id_to_path(self, image_id: str) -> str:
        pass


class IdenticalConvertor(ImageIdToImagePathConvertor):
    def id_to_path(self, image_id: str) -> str:
        return image_id


DEFAULT = IdenticalConvertor()


class ImageService:
    def __init__(self, id_to_path_convertor: ImageIdToImagePathConvertor = DEFAULT):
        self._convertor = id_to_path_convertor

    def get_image_by_id(self, image_id):
        with open(resource_path(self._convertor.id_to_path(image_id)), READ_BYTES) as file:
            return file.read()
