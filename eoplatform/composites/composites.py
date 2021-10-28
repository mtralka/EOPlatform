# type: ignore[override]

from abc import ABC
from abc import abstractclassmethod
from abc import abstractmethod
from typing import cast

from eoplatform.console import console
import numpy as np
import numpy.typing as npt
from rich.panel import Panel
from rich.text import Text


class Composite(ABC):
    @classmethod
    def info(cls) -> None:
        console.print(
            Panel(
                Text(cast(str, cls.__doc__), justify="full"),
                expand=False,
                title=cls.__name__,
                width=100,
            )
        )

    @staticmethod
    def create() -> None:
        raise NotImplementedError()


class NDVI(Composite):
    """
    Normalized Difference Vegetation Index (NDVI)
    NDVI values range from -1 to +1
    A low value represents an area of baren land
    A high value represents dense vegetation
    """

    @staticmethod
    def create(NIR: npt.NDArray, RED: npt.NDArray) -> npt.NDArray:

        if NIR.shape != RED.shape:
            raise ValueError("Arrays must be the same shape")

        return (NIR.astype(float) - RED.astype(float)) / (NIR + RED + 1e-7)


class SR(Composite):
    """
    Simple Ratio (SR)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, RED: npt.NDArray) -> npt.NDArray:

        if NIR.shape != RED.shape:
            raise ValueError("Arrays must be the same shape")

        return NIR.astype(float) / (RED.astype(float) + 1e-7)


class DVI(Composite):
    """
    Difference Vegetation Index (DVI)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, RED: npt.NDArray) -> npt.NDArray:

        if NIR.shape != RED.shape:
            raise ValueError("Arrays must be the same shape")

        return NIR.astype(float) - RED.astype(float)


class EVI(Composite):
    """
    Enhanced Vegetation Index (EVI)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, RED: npt.NDArray, BLUE: npt.NDArray) -> npt.NDArray:

        if NIR.shape != RED.shape != BLUE.shape:
            raise ValueError("Arrays must be the same shape")

        return 2.5 * ((NIR - RED).astype(float) / (NIR + (6 * RED) - (7.5 * BLUE) + 1))


class EVI2(Composite):
    """
    Enhanced Vegetation Index 2 (EVI2)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, RED: npt.NDArray) -> npt.NDArray:

        if NIR.shape != RED.shape:
            raise ValueError("Arrays must be the same shape")

        return 2.5 * ((NIR - RED).astype(float) / (NIR + (2.4 * RED) + 1))


class NDWI(Composite):
    """
    Normalized Difference Water Index (NDWI)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, GREEN: npt.NDArray) -> npt.NDArray:

        if NIR.shape != GREEN.shape:
            raise ValueError("Arrays must be the same shape")

        return (GREEN - NIR).astype(float) / (GREEN + NIR).astype(float)


class NBR(Composite):
    """
    Normalized Burn Ratio (NBR)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, SWIR2: npt.NDArray) -> npt.NDArray:

        if NIR.shape != SWIR2.shape:
            raise ValueError("Arrays must be the same shape")

        return (NIR - SWIR2).astype(float) / (NIR + SWIR2)


class NDSI:
    """
    Normalized Difference Snow Index (NDSI)
    ...
    """

    @staticmethod
    def create(GREEN: npt.NDArray, SWIR1: npt.NDArray) -> npt.NDArray:

        if GREEN.shape != SWIR1.shape:
            raise ValueError("Arrays must be the same shape")

        return (GREEN - SWIR1).astype(float) / (GREEN + SWIR1)


class NDBI(Composite):
    """
    Normalized Difference Built-Up Index (NDBI)
    ...
    """

    @staticmethod
    def create(NIR: npt.NDArray, SWIR1: npt.NDArray) -> npt.NDArray:

        if NIR.shape != SWIR1.shape:
            raise ValueError("Arrays must be the same shape")

        return (SWIR1 - NIR).astype(float) / (SWIR1 + NIR)
