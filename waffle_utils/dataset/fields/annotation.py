from typing import Union

from waffle_utils.utils import type_validator

from .base_field import BaseField


class Annotation(BaseField):
    def __init__(
        self,
        # required
        annotation_id: int,
        image_id: int,
        # optional
        category_id: int = None,
        bbox: list[float] = None,
        segmentation: list[float] = None,
        area: float = None,
        keypoints: list[float] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        #
        iscrowd: int = None,
        score: Union[float, list[float]] = None
    ):

        self.annotation_id = annotation_id
        self.image_id = image_id
        self.category_id = category_id
        self.bbox = bbox
        self.segmentation = segmentation
        self.area = area
        self.keypoints = keypoints
        self.num_keypoints = num_keypoints
        self.caption = caption
        self.value = value
        self.iscrowd = iscrowd
        self.score = score

    # properties
    @property
    def annotation_id(self):
        return self.__annotation_id

    @annotation_id.setter
    @type_validator(int)
    def annotation_id(self, v):
        if v is None:
            raise ValueError("annotation_id should not be None")
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__annotation_id = v

    @property
    def image_id(self):
        return self.__image_id

    @image_id.setter
    @type_validator(int)
    def image_id(self, v):
        if v is None:
            raise ValueError("image_id should not be None")
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__image_id = v

    @property
    def category_id(self):
        return self.__category_id

    @category_id.setter
    @type_validator(int)
    def category_id(self, v):
        if v and v < 1:
            raise ValueError("id should be greater than 0.")
        self.__category_id = v

    @property
    def bbox(self):
        return self.__bbox

    @bbox.setter
    @type_validator(list)
    def bbox(self, v):
        if v and len(v) != 4:
            raise ValueError("the length of bbox should be 4.")
        self.__bbox = v

    @property
    def segmentation(self):
        return self.__segmentation

    @segmentation.setter
    @type_validator(list)
    def segmentation(self, v):
        if v and len(v) % 2 != 0 and len(v) < 6:
            raise ValueError(
                "the length of segmentation should be at least 6 and divisible by 2."
            )
        self.__segmentation = v

    @property
    def area(self):
        return self.__area

    @area.setter
    @type_validator(float, strict=False)
    def area(self, v):
        self.__area = v

    @property
    def keypoints(self):
        return self.__keypoints

    @keypoints.setter
    @type_validator(list)
    def keypoints(self, v):
        if v and len(v) % 3 != 0 and len(v) < 2:
            raise ValueError(
                "the length of keypoints should be at least 2 and divisible by 3."
            )
        self.__keypoints = v

    @property
    def num_keypoints(self):
        return self.__num_keypoints

    @num_keypoints.setter
    @type_validator(int)
    def num_keypoints(self, v):
        self.__num_keypoints = v

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    @type_validator(str)
    def caption(self, v):
        self.__caption = v

    @property
    def value(self):
        return self.__value

    @value.setter
    @type_validator(float)
    def value(self, v):
        self.__value = v

    @property
    def iscrowd(self):
        return self.__iscrowd

    @iscrowd.setter
    @type_validator(int)
    def iscrowd(self, v):
        self.__iscrowd = v

    @property
    def score(self):
        return self.__score

    @score.setter
    # @type_validator(float)  # TODO: need to upgrade type_validator
    def score(self, v):
        self.__score = v

    # factories
    @classmethod
    def new(
        cls,
        annotation_id: int,
        image_id: int,
        category_id: int = None,
        bbox: list[float] = None,
        segmentation: list[float] = None,
        area: int = None,
        keypoints: list[float] = None,
        num_keypoints: int = None,
        caption: str = None,
        value: float = None,
        iscrowd: int = None,
        score: float = None
    ) -> "Annotation":
        """Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            segmentation (list[float]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): bbox area.
            keypoints (list[float]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            caption (str): string.
            value (float): regression value.
            iscrowd (int, optional): is crowd or not. Default to None.
            score (float, optional): prediction score. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(
            annotation_id=annotation_id,
            image_id=image_id,
            category_id=category_id,
            bbox=bbox,
            segmentation=segmentation,
            area=area,
            keypoints=keypoints,
            num_keypoints=num_keypoints,
            caption=caption,
            value=value,
            iscrowd=iscrowd,
            score=score
        )

    @classmethod
    def classification(
        cls, annotation_id: int, image_id: int, category_id: int, score: float = None
    ) -> "Annotation":
        """Classification Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            score (float, optional): prediction score. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(annotation_id, image_id, category_id=category_id, score=score)

    @classmethod
    def object_detection(
        cls,
        annotation_id: int,
        image_id: int,
        category_id: int,
        bbox: list[float],
        area: int,
        iscrowd: int = 0,
        score: float = None
    ) -> "Annotation":
        """Object Detection Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            area (int): bbox area.
            iscrowd (int, optional): is crowd or not. Default to 0.
            score (float, optional): prediction score. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(
            annotation_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            area=area,
            iscrowd=iscrowd,
            score=score,
        )

    @classmethod
    def segmentation(
        cls,
        annotation_id: int,
        image_id: int,
        category_id: int,
        bbox: list[float],
        segmentation: list[float],
        area: int,
        iscrowd: int = 0,
        score: float = None
    ) -> "Annotation":
        """Segmentation Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            segmentation (list[float]): [x1, y1, x2, y2, x3, y3, ...].
            area (int): segmentation segmentation area.
            iscrowd (int, optional): is crowd or not. Default to 0.
            score (float, optional): prediction score. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(
            annotation_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            segmentation=segmentation,
            area=area,
            iscrowd=iscrowd,
            score=score,
        )

    @classmethod
    def keypoint_detection(
        cls,
        annotation_id: int,
        image_id: int,
        category_id: int,
        bbox: list[float],
        keypoints: list[float],
        num_keypoints: int,
        area: int,
        segmentation: list[float] = None,
        iscrowd: int = 0,
        score: list[float] = None
    ) -> "Annotation":
        """Keypoint Detection Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            bbox (list[float]): [x1, y1, w, h].
            keypoints (list[float]):
                [x1, y1, v1(visible flag), x2, y2, v2(visible flag), ...].
                visible flag is one of [0(Not labeled), 1(Labeled but not visible), 2(labeled and visible)]
            num_keypoints: number of labeled keypoints
            area (int): segmentation segmentation or bbox area.
            segmentation (list[float], optional): [x1, y1, x2, y2, x3, y3, ...].
            iscrowd (int, optional): is crowd or not. Default to 0.
            score (list[float], optional): prediction scores. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(
            annotation_id,
            image_id,
            category_id=category_id,
            bbox=bbox,
            keypoints=keypoints,
            num_keypoints=num_keypoints,
            segmentation=segmentation,
            area=area,
            iscrowd=iscrowd,
            score=score
        )

    @classmethod
    def regression(
        cls, annotation_id: int, image_id: int, value: float
    ) -> "Annotation":
        """Regression Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            value (float): regression value.

        Returns:
            Annotation: annotation class
        """
        return cls(annotation_id, image_id, value=value)

    @classmethod
    def text_recognition(
        cls, annotation_id: int, image_id: int, caption: str, score: float = None
    ) -> "Annotation":
        """Text Recognition Annotation Format

        Args:
            annotation_id (int): annotaion id. natural number.
            image_id (int): image id. natural number.
            category_id (int): category id. natural number.
            caption (str): string.
            score (float, optional): prediction score. Default to None.

        Returns:
            Annotation: annotation class
        """
        return cls(annotation_id, image_id, caption=caption, score=score)

    def to_dict(self) -> dict:
        """Get Dictionary of Annotation Data

        Returns:
            dict: annotation dictionary.
        """

        ann = {"annotation_id": self.annotation_id, "image_id": self.image_id}

        if self.category_id is not None:
            ann["category_id"] = self.category_id
        if self.bbox is not None:
            ann["bbox"] = self.bbox
        if self.segmentation is not None:
            ann["segmentation"] = self.segmentation
        if self.area is not None:
            ann["area"] = self.area
        if self.keypoints is not None:
            ann["keypoints"] = self.keypoints
        if self.caption is not None:
            ann["caption"] = self.caption
        if self.value is not None:
            ann["value"] = self.value
        if self.iscrowd is not None:
            ann["iscrowd"] = self.iscrowd
        if self.score is not None:
            ann["score"] = self.score

        return ann

    def is_prediction(self):
        return not self.score is None
