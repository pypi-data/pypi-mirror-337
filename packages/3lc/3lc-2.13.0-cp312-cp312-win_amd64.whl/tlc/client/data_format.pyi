import numpy as np
from numpy.typing import NDArray as NDArray
from typing import TypedDict

class InstanceSegmentationDict(TypedDict):
    """The base class for dictionary representations of instance segmentation data."""
    image_height: int
    image_width: int
    instance_properties: dict[str, dict | list]

class SegmentationPolygonsDict(InstanceSegmentationDict):
    """A dictionary representation of instance segmentation data where each instance is represented by a list of
    polygons.
    """
    polygons: list[list[float]]

class SegmentationMasksDict(InstanceSegmentationDict):
    """A dictionary representation of instance segmentation data where each instance is represented by a binary mask."""
    masks: NDArray[np.uint8]

class _InternalInstanceSegmentationDict(TypedDict):
    """An internal dictionary representation of instance segmentation data."""
    image_height: int
    image_width: int
    instance_properties: dict[str, dict | list]
    rles: list[bytes]
